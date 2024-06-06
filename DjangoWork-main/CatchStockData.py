# twstock 套件要額外在 CMD 安裝 
import twstock, django
from django.conf import settings

# 使用獨立於 Django 專案之外的程式碼，需要手動設置 Django 環境 
settings.configure(
    DEBUG=True,  # 根據需要設置其他設定
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',  # 資料庫配置
        }
    },
    INSTALLED_APPS=[
        'Stock',  # 專案名稱
    ]
)

# 初始化 Django
django.setup()


from Stock.models import stock_data 

# 要爬取的股票代碼列表
stock_symbols = ['2330', '2317', '2454', '1301', '1303', '2412', '2308', '2881', '2891', '2892']

t = 0
# 爬取每支股票的歷史資訊並存入資料庫
for symbol in stock_symbols:
    stock = twstock.Stock(symbol)
    historical_data = stock.fetch_from(2023, 4) #2023/4/到現在

    for data in historical_data:
        stock_data.objects.update_or_create(
            stock_symbol=symbol,
            date=data.date,
            defaults={
                'total_capacity': data.capacity,
                'total_turnover': data.turnover,
                'open_price': data.open,
                'high_price': data.high,
                'low_price': data.low,
                'close_price': data.close,
                'change_price': data.change,
                'trans_action': data.transaction
            }
        )
    t += 1
    print("已存入 %d 筆"%(t))

print("資料已成功存入資料庫")
