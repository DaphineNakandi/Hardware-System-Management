from django.contrib import admin
from .models  import Product, StockEntry, Sale, Supplier, DepositCustomer, DepositPayment, DepositWithdrawal

# Register your models here.
admin.site.register(Product)
admin.site.register(StockEntry)
admin.site.register(Sale)
admin.site.register(Supplier)
admin.site.register(DepositCustomer)
admin.site.register(DepositPayment)
admin.site.register(DepositWithdrawal)