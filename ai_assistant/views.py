import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def fetch_mock_news(asset_or_query):
    return f"Recent news shows high volatility in {asset_or_query} due to macroeconomic factors."

def fetch_mock_openai_explanation(user_query, news_context):
    if "predict" in user_query.lower() or "next" in user_query.lower():
        return "I am an analytical AI. I can only explain past market movements based on news context. I cannot predict future prices."
    return f"Based on recent data, the movement in the market is largely attributed to institutional positioning. {news_context} Please note this is an analysis of past events, not financial advice."

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            news_context = fetch_mock_news("the market")
            ai_response = fetch_mock_openai_explanation(user_message, news_context)
            return JsonResponse({"status": "success", "response": ai_response})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "invalid request"}, status=405)
