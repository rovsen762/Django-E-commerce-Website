
from . import views
from django.urls import path



urlpatterns = [
    path('', views.store , name='store'),
    path('categories/<slug:category_slug>', views.category_list , name='products_by_category'),
    path('<slug:category_slug>/<int:product_id>', views.product, name='product'),
    path('add_to_cart/<slug:slug>', views.add_to_cart, name='add_to_cart'),
    path('increase_cart/<slug:slug>', views.increase_cart, name='increase_cart'),
    path('decrease_cart/<slug:slug>', views.decrease_cart, name='decrease_cart'),
    path('store_cart/', views.StoreCart.as_view(), name='store_cart'),
    path('remove_from_cart/<slug:slug>',views.remove_from_cart,name='remove_from_cart'),
    path('order_checkout/', views.OrderCheckout.as_view(), name='order_checkout'),
    path('orders/', views.Orders.as_view(), name='orders'),
    path('order_detail/<int:order_id>/', views.OrderDetail.as_view(), name='order_detail'),
]