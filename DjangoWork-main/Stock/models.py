from django.db import models


'''
資料庫結構名稱意義對照表:

stock_symbol: 股票編號
date  : 日期
total_capacity: 總成交股數
total_turnover: 總成交金額
open_price: 開盤價
high_price: 盤中最高價
low_price : 盤中最低價
close_price:  收盤價
change_price: 漲跌價差
trans_action:  成交筆數
'''
class stock_data(models.Model):
    stock_symbol    = models.CharField(max_length=10)
    date            = models.CharField(max_length=25)
    total_capacity  = models.IntegerField()
    total_turnover  = models.DecimalField(max_digits=20, decimal_places=2)
    open_price      = models.DecimalField(max_digits=10, decimal_places=2)
    high_price      = models.DecimalField(max_digits=10, decimal_places=2)
    low_price       = models.DecimalField(max_digits=10, decimal_places=2)
    close_price     = models.DecimalField(max_digits=10, decimal_places=2)
    change_price    = models.DecimalField(max_digits=10, decimal_places=2)
    trans_action    = models.IntegerField()

    def __str__(self):
        return self.stock_symbol 
class stock_info(models.Model):
    stock_renew_date = models.CharField(max_length=25 , null=True, blank=True)
