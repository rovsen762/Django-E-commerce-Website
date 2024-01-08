from django.contrib import admin
from .models import Category,Product,CartItem,Cart,OrderProduct,Order
from django.contrib.auth import logout
from django.shortcuts import redirect

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'in_stock']
    list_filter = ['category', 'in_stock']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['get_total_item_price']
    fields = ['product', 'quantity', 'get_total_item_price']

    def get_total_item_price(self, instance):
        return instance.get_total_item_price()
    get_total_item_price.short_description = 'Total Product Price'



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'get_total_cart_price']
    inlines = [CartItemInline]

    def get_total_cart_price(self, obj):
        return CartItem.get_total_cart_price(obj)
    
    get_total_cart_price.short_description = 'Total Cart Price'



class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['get_total_item_price']
    fields = ['products', 'quantity', 'get_total_item_price']
    extra = 0

    def get_total_item_price(self, instance):
        return instance.get_total_item_price()
    get_total_item_price.short_description = 'Total Product Price'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','first_name','last_name','get_total_order_price','created_at']
    list_filter = ['customer','phone','email']
    inlines = [OrderProductInline]

    def get_total_order_price(self, obj):
        order_products = obj.orderproduct_set.all()
        total_price = sum(item.get_total_item_price() for item in order_products)
        return total_price
    get_total_order_price.short_description = 'Total Order Price'







