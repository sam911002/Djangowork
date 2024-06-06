from django.shortcuts import render
from Stock.models import stock_data, stock_info
from django.http import JsonResponse
import twstock
from datetime import datetime
import json

def get(request):
    stock_symbols = [
        "2330",
        "2317",
        "2454",
        "1301",
        "1303",
        "2412",
        "2308",
        "2881",
        "2891",
        "2892",
    ]
    
    for symbol in stock_symbols:
        stock = twstock.Stock(symbol)
        stock_info_record, created = stock_info.objects.get_or_create()
        if created or not stock_info_record.stock_renew_date:
            start_year = 2023
            start_month = 4
        else:
            last_update = datetime.strptime(stock_info_record.stock_renew_date, '%Y-%m-%d')
            start_year = last_update.year
            start_month = last_update.month
        
        historical_data = stock.fetch_from(start_year, start_month)
        for data in historical_data:
            stock_data.objects.update_or_create(
                stock_symbol=symbol,
                date=data.date,
                defaults={
                    "total_capacity": data.capacity,
                    "total_turnover": data.turnover,
                    "open_price": data.open,
                    "high_price": data.high,
                    "low_price": data.low,
                    "close_price": data.close,
                    "change_price": data.change,
                    "trans_action": data.transaction,
                },
            )
    if historical_data:
        last_date = historical_data[-1].date.strftime('%Y-%m-%d')
        stock_info_record.stock_renew_date = last_date
        stock_info_record.save()
    data = {"message": "資料已成功存入資料庫"}
    return JsonResponse(data)

def home(request):
    try:
        Stock_Symbol = request.GET.get("stock_symbol")
        unit = stock_data.objects.filter(stock_symbol=Stock_Symbol).last()
        data_dict = {
            "2330": {
                "image": "image/2330.jpg",
                "title": "2330 臺灣積體電路",
                "description": "臺灣積體電路製造公司，簡稱TSMC、臺積電、臺積或臺積公司，為臺灣一家從事晶圓代工的公司。",
                "url": "?stock_symbol=2330",
            },
            "2317": {
                "image": "image/2317.png",
                "title": "2317 鴻海精密工業",
                "description": "鴻海精密工業是臺灣電子製造公司，也是鴻海科技集團的核心企業。",
                "url": "?stock_symbol=2317",
            },
            "2454": {
                "image": "image/2454.jpg",
                "title": "2454 聯發科技",
                "description": "聯發科技，簡稱聯發科，是臺灣一家為無線通訊、高畫質電視設計系統晶片的無廠半導體公司。",
                "url": "?stock_symbol=2454",
            },
            "1301": {
                "image": "image/1301.jpg",
                "title": "1301 台灣塑膠工業",
                "description": "台塑工業股份有限公司是一家位於台灣的塑膠公司，主要生產聚氯乙烯樹脂和其他塑膠產品。",
                "url": "?stock_symbol=1301",
            },
            "1303": {
                "image": "image/1303.jpg",
                "title": "1303 南亞塑膠",
                "description": "南亞塑膠工業股份有限公司簡稱南亞、南亞塑膠，是台灣一家塑膠公司，1958年創立。",
                "url": "?stock_symbol=1303",
            },
            "2412": {
                "image": "image/2412.jpg",
                "title": "2412 中華電信",
                "description": "中華電信是臺灣綜合電信服務業者之一，前身為交通部電信總局的營運部門。",
                "url": "?stock_symbol=2412",
            },
            "2308": {
                "image": "image/2308.jpg",
                "title": "2308 台達電子",
                "description": "台達電子工業股份有限公司，是一家臺灣的電子製造公司。",
                "url": "?stock_symbol=2308",
            },
            "2881": {
                "image": "image/2881.jpg",
                "title": "2881 富邦金融",
                "description": "富邦金融控股股份有限公司是一家臺灣的金融控股公司。",
                "url": "?stock_symbol=2881",
            },
            "2891": {
                "image": "image/2891.png",
                "title": "2891 中國信託",
                "description": "中國信託金融控股股份有限公司是臺灣的金融控股公司之一。",
                "url": "?stock_symbol=2891",
            },
            "2892": {
                "image": "image/2892.png",
                "title": "2892 第一金控",
                "description": "第一金融控股為臺灣的金融控股公司於2003年1月2日以第一商業銀行為主體，由股份轉換方式成立。",
                "url": "?stock_symbol=2892",
            },
        }
    except:
        print("Error")
    return render(request, "index.html", {"Data": data_dict})

def search(request):
    data_dict = {}
    error_message = None 
    try:
        Stock_Symbol = request.GET.get("stock_symbol")
        twstock.realtime.mock = False
        unit = twstock.realtime.get(Stock_Symbol)
        first_date = stock_data.objects.order_by('date').values_list('date', flat=True).first()
        last_date = stock_data.objects.order_by('-date').values_list('date', flat=True).first()
        first_date = first_date.split()[0]
        last_date = last_date.split()[0]
        first_date = datetime.strptime(first_date, '%Y-%m-%d')
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        first_year = first_date.year
        last_year = last_date.year
        first_month = first_date.month
        last_month = last_date.month
        all_year = [i for i in range(first_year, last_year + 1)]
        all_month = {i: [j for j in range(1, 13)] for i in all_year}
        all_month[first_year] = [i for i in range(first_month, 13)]
        all_month[last_year] = [i for i in range(1, last_month + 1)]
        time = datetime.utcfromtimestamp(unit['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        stock_symbol = unit["info"]["code"]
        name = unit["info"]["name"]
        fullname = unit["info"]["fullname"]
        best_bit_price = [str(price).rstrip('0').rstrip('.') if '.' in str(price) else str(price) for price in unit["realtime"]["best_bid_price"]]
        best_bit_volume = list(map(str, unit["realtime"]["best_bid_volume"]))
        best_ask_price = [str(price).rstrip('0').rstrip('.') if '.' in str(price) else str(price) for price in unit["realtime"]["best_ask_price"]]
        best_ask_volume = list(map(str, unit["realtime"]["best_ask_volume"]))
        open_price = str(unit["realtime"]["open"]).rstrip('0').rstrip('.') if '.' in str(unit["realtime"]["open"]) else str(unit["realtime"]["open"])
        high_price = str(unit["realtime"]["high"]).rstrip('0').rstrip('.') if '.' in str(unit["realtime"]["high"]) else str(unit["realtime"]["high"])
        low_price = str(unit["realtime"]["low"]).rstrip('0').rstrip('.') if '.' in str(unit["realtime"]["low"]) else str(unit["realtime"]["low"])
        stock_back = Stock_Symbol in ["2330", "2317", "2454", "1301", "1303", "2412", "2308", "2881", "2891", "2892"]
        data_dict = {
            "time": time,
            "stock_symbol": stock_symbol,
            "name": name,
            "fullname": fullname,
            "best_bit_price": best_bit_price,
            "best_bit_volume": best_bit_volume,
            "best_ask_price": best_ask_price,
            "best_ask_volume": best_ask_volume,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "last_date": last_date,
            "first_date": first_date,
            "all_month": all_month,
            "all_year": all_year,
            "stock_back": stock_back,
        }
    except Exception as e:
        print("Error: ", e)
        error_message = "查無此資料"
    return render(request, "get_stock.html", {"Data": data_dict, "error_message": error_message})

def get_stock(request):
    error_message = None
    Data = None
    if request.method == 'POST':
        stock_symbol = request.POST['stock_symbol']
        try:
            stock_real_time = twstock.realtime.get(stock_symbol)
            if stock_real_time['success']:
                stock_back = twstock.Stock(stock_symbol)
                all_year = list(range(stock_back.fetch_from.year, datetime.now().year + 1))
                all_month = {str(year): list(range(1, 13)) for year in all_year}
                Data = {
                    'fullname': stock_real_time['info']['fullname'],
                    'name': stock_real_time['info']['name'],
                    'stock_symbol': stock_symbol,
                    'time': stock_real_time['info']['time'],
                    'open': stock_real_time['realtime']['open'],
                    'high': stock_real_time['realtime']['high'],
                    'low': stock_real_time['realtime']['low'],
                    'best_bit_price': stock_real_time['realtime']['best_bid_price'],
                    'best_bit_volume': stock_real_time['realtime']['best_bid_volume'],
                    'best_ask_price': stock_real_time['realtime']['best_ask_price'],
                    'best_ask_volume': stock_real_time['realtime']['best_ask_volume'],
                    'stock_back': True,
                    'all_year': all_year,
                    'all_month': all_month
                }
            else:
                error_message = '查無此股票'
        except Exception as e:
            error_message = str(e)
    return render(request, 'Stock/get_stock.html', {'error_message': error_message, 'Data': Data})

def get_historical_data(request):
    stock_symbol = request.GET.get('stock_symbol')
    year = int(request.GET.get('year'))
    month = request.GET.get('month', None)
    
    stock_back = twstock.Stock(stock_symbol)
    historical_data = []
    if month:
        stock_data = stock_back.fetch(year, int(month))
    else:
        stock_data = []
        for m in range(1, 13):
            stock_data.extend(stock_back.fetch(year, m))
    for data in stock_data:
        historical_data.append({
            'date': data.date.strftime('%Y-%m-%d'),
            'close_price': data.close
        })
    return JsonResponse({'historical_data': historical_data})
