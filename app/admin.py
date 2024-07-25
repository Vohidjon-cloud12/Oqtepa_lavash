from django.contrib import admin
from .models import Product, Order

# Modellarni admin interfeysiga ro'yxatdan o'tkazish
admin.site.register(Product)
admin.site.register(Order)

from django.contrib import admin
from .models import Product, Order


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'sold_date')
    list_filter = ('sold_date', 'customer')
    search_fields = ('customer',)
