import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from openai import OpenAI

# Initialize the OpenAI client using the key from settings.py
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def fetch_financial_news(query):
    """Fetches real-time news from GNews API based on the user's query."""
    api_key = settings.NEWS_API_KEY
    if not api_key:
        return "No news API key configured."
    
    # We use a broad search term if the query is too short, or the user query itself
    search_term = query if len(query) > 3 else "financial markets"
    url = f"https://gnews.io/api/v4/search?q={search_term}&lang=en&max=3&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        
        if not articles:
            return f"No recent news found for '{search_term}'."
        
        # Format the top articles into a readable string for OpenAI
        news_context = "Recent News Highlights:\n"
        for i, article in enumerate(articles, 1):
            news_context += f"{i}. {article.get('title')} - {article.get('description')} (Source: {article.get('source', {}).get('name')})\n"
        return news_context
        
    except Exception as e:
        return f"Error fetching news context: {str(e)}"

def fetch_openai_explanation(user_query, news_context):
    """Sends the user query and news context to OpenAI for reasoning."""
    system_prompt = (
        "You are a professional, highly analytical financial AI assistant. "
        "Use the provided recent news context to answer the user's query accurately and explain past/current market movements. "
        "Strict Rule: Do NOT predict future prices. If a user asks for a prediction, politely explain that you can only analyze current data and past events."
    )
    
    user_prompt = f"Context:\n{news_context}\n\nUser Query: {user_query}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # You can change this to "gpt-4o" if you prefer
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # Low temperature keeps it analytical and grounded
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI service: {str(e)}"

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            
            # 1. Fetch live news context based on the user's message
            news_context = fetch_financial_news(user_message)
            
            # 2. Get AI Explanation using the real OpenAI API
            ai_response = fetch_openai_explanation(user_message, news_context)
            
            return JsonResponse({"status": "success", "response": ai_response})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "invalid request"}, status=405)
