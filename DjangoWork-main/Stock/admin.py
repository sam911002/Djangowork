from django.contrib import admin
from .models import stock_data , stock_info

class Stock_dataadmin(admin.ModelAdmin):
    list_display = ('stock_symbol', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'change_price')
    search_fields = ('stock_symbol', 'date')
    pass
                    
admin.site.register(stock_data, Stock_dataadmin)
admin.site.register(stock_info)
