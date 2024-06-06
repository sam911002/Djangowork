import twstock

data_dict = {}

twstock.realtime.mock = False
unit = twstock.realtime.get("2330")

# unit = stock_data.objects.filter(
#     stock_symbol=Stock_Symbol
# ).last()  # 讀取一筆資料

# 打包到字典
data_dict = {
    "time": unit["timestamp"],
    "stock_symbol": unit["info"]["code"],
    "name": unit["info"]["name"],
    "fullname": unit["info"]["fullname"],
    "best_bit_price": unit["realtime"]["best_bid_price"],
    # "best_bit_volume": unit["realtime"]["best_bit_volume"],
    # "best_ask_price": unit["realtime"]["best_ask_price"],
    # "best_ask_volume": unit["realtime"]["best_ask_volume"],
    "open": unit["realtime"]["open"],
    "high": unit["realtime"]["high"],
    "low": unit["realtime"]["low"],
    "X": unit["success"],
}
print(data_dict)
