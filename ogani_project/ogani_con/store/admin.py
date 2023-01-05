from django.contrib import admin
from .models import Category, Product, OrderProduct, Order , CheckoutAddress
from django.contrib.auth import logout
from django.shortcuts import redirect

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'in_stock']
    list_filter = ['category', 'in_stock']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(OrderProduct)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity','get_total_item_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'ordered', 'get_total',]

    def total(self, obj):
        return obj.get_total()

@admin.register(CheckoutAddress)
class CheckoutAddressAdmin(admin.ModelAdmin):
    list_display = ['customer','first_name', 'last_name', 'address', 'phone', 'email']


