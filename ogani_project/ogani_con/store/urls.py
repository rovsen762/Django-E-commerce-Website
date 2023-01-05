from django.urls import path
from . import views


urlpatterns = [
    path('', views.store , name='store'),
    path('categories/<slug:category_slug>', views.category_list , name='products_by_category'),
    path('<slug:category_slug>/<int:product_id>', views.product, name='product'),
    path('add_to_cart/<slug:slug>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:slug>', views.remove_from_cart, name='remove_from_cart'),
    path('store_cart/', views.StoreCart.as_view(), name='store_cart'),
    path('store_checkout/', views.StoreCheckout.as_view(), name='store_checkout'),

]