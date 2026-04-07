import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from groq import Groq

# Initialize the Groq client using the key from settings.py
# (Ensure settings.GROQ_API_KEY is properly pulling from os.getenv('GROQ_API_KEY'))
client = Groq(api_key=settings.GROQ_API_KEY)

def fetch_financial_news(query):
    """Fetches real-time news from GNews API based on the user's query."""
    api_key = getattr(settings, 'NEWS_API_KEY', None)
    print(f"API Key: {api_key}")
    if not api_key:
        return "No news API key configured."
    
    # Convert the natural language query into keywords
    keywords = " ".join([word for word in query.split() if len(word) > 3])
    # Fallback if keywords are too short
    search_term = keywords if keywords else "bitcoin price"
    
    url = f"https://newsapi.org/v2/everything?q={search_term}&language=en&pageSize=20&sortBy=publishedAt&apikey={api_key}"
    print(f"Fetching news for: {search_term} using URL: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        #articles = articles[:20]
        
        
        
        if not articles:
            return f"No recent news found for '{search_term}'."
        
        news_context = "Recent News Highlights:\n"
        for i, article in enumerate(articles, 1):
            title = article.get('title')
            description = article.get('description')
            source = article.get('source', {}).get('name')
            url = article.get('url')
            news_context += (
                f"ARTICLE {i}:\n" 
                f"TITLE: {title}\n"
                f"SUMMARY: {description}\n"
                f"SOURCE: {source}\n"
                f"URL: {url}\n\n"
            )
        
        return news_context
        
    except Exception as e:
        return f"Error fetching news context: {str(e)}"

def fetch_groq_explanation(user_query, news_context):
    """Sends the user query and news context to Groq for reasoning."""
    system_prompt = (
        "You are a professional, highly analytical financial AI assistant. "
        "You MUST follow these strict rules:\n"
        
    "1. You MUST only use the provided articles.\n"
    "2. Each article is labeled as ARTICLE 1, ARTICLE 2, etc.\n"
    "3. When referencing, you MUST use [1], [2], etc (matching ARTICLE numbers).\n"
    "4. You MUST NOT invent numbers like [7] or [25].\n"
    "5. You MUST include ALL referenced articles in the Sources section.\n"
    "6. You MUST include:\n"
    "   - Article title\n"
    "   - Source name (e.g. CNN, Reuters)\n"
    "   - Full URL\n\n"

    "FINAL OUTPUT FORMAT:\n"
    "Answer...\n\n"
    "Sources:\n"
    "[1] Title - Source Name - URL\n"
    "[2] Title - Source Name - URL\n"

        "Do NOT predict future prices. Only analyze based on provided data."
    )
    
    user_prompt = (
        f"Here is recent financial news:\n\n{news_context}\n\n"
        f"User question: {user_query}\n\n"
        "Answer using ONLY these articles.\n"
        "Cite using [ARTICLE NUMBER].\n"
        "At the end, list ALL used sources with title, source name, and URL."
    )
    
    try:
        # Groq's SDK syntax is virtually identical to OpenAI's!
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # A highly capable and incredibly fast Groq model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # Low temperature keeps it analytical and grounded
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq service: {str(e)}"

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            
            # 1. Fetch live news context based on the user's message
            news_context = fetch_financial_news(user_message)
            
            # 2. Get AI Explanation using the Groq API
            ai_response = fetch_groq_explanation(user_message, news_context)
            
            return JsonResponse({"status": "success", "response": ai_response})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "invalid request"}, status=405) #@@