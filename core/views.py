from django.shortcuts import render, redirect
from .forms import SignupForm

def home(request):
    return render(request, 'core/home.html')

def charts(request):
    PRESET_SYMBOLS = [
        'BINANCE:BTCUSDT','BINANCE:ETHUSDT','BINANCE:BNBUSDT','BINANCE:SOLUSDT','BINANCE:XRPUSDT',
        'OANDA:EURUSD','OANDA:USDJPY','OANDA:GBPUSD','OANDA:USDCHF','OANDA:AUDUSD',
        'NASDAQ:AAPL','NASDAQ:TSLA','NASDAQ:MSFT','NASDAQ:AMZN','NASDAQ:NVDA',
        'TVC:GOLD','TVC:SILVER','TVC:USOIL','TVC:UKOIL',
        'OANDA:NAS100USD','OANDA:SPX500USD','OANDA:US30USD','OANDA:JP225USD','OANDA:UK100GBP'
    ]
    preset = request.GET.get("preset_symbol")
    search = request.GET.get("symbol")

    if preset:
        symbol = preset
    elif search:
        symbol = search
    else:
        symbol = "BINANCE:BTCUSDT"
    # Only show search value if user typed something
    if search and search not in PRESET_SYMBOLS:
        search_value = search
    else:
        search_value = ""
    is_custom = symbol not in PRESET_SYMBOLS
    return render(request, 'core/charts.html', {'symbol': symbol, 'is_custom': is_custom, 'search_value': search_value})

def calendar(request):
    events = [
        {"time": "08:30 AM", "event": "Non Farm Payrolls", "currency": "USD", "impact": "High"},
        {"time": "10:00 AM", "event": "ISM Manufacturing PMI", "currency": "USD", "impact": "Medium"},
        {"time": "04:00 AM", "event": "ECB Interest Rate Decision", "currency": "EUR", "impact": "High"},
        {"time": "12:30 PM", "event": "Crude Oil Inventories", "currency": "USD", "impact": "Low"},
    ]
    return render(request, 'core/calendar.html', {'events': events})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })
