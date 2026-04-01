from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def charts(request):
    symbol = request.GET.get('symbol', 'BINANCE:BTCUSDT')
    return render(request, 'charts.html', {'symbol': symbol})

def calendar(request):
    events = [
        {"time": "08:30 AM", "event": "Non Farm Payrolls", "currency": "USD", "impact": "High"},
        {"time": "10:00 AM", "event": "ISM Manufacturing PMI", "currency": "USD", "impact": "Medium"},
        {"time": "04:00 AM", "event": "ECB Interest Rate Decision", "currency": "EUR", "impact": "High"},
        {"time": "12:30 PM", "event": "Crude Oil Inventories", "currency": "USD", "impact": "Low"},
    ]
    return render(request, 'calendar.html', {'events': events})
