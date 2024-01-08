from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product,Category,Cart,CartItem,OrderProduct,Order
from blogs.models import Blog
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderCheckoutForm
import json



# Create your views here.

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    blogs = Blog.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'blogs': blogs
    }
    return render(request, 'store.html', context)

def category_list(request, category_slug):
    products = Product.objects.all().filter(category__slug = category_slug)
    categories = Category.objects.all()
    context = {
        
        'products': products,
        'categories': categories
    }
    return render(request, 'store.html', context)

def product(request, category_slug , product_id):
    recent_products = Product.objects.all().order_by('-date')[:4]
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'recent_products': recent_products
    }
    return render(request, 'product.html', context)



@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug) 
    customer = request.user

    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, is_active=True)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('store_cart')



@login_required
def increase_cart(request, slug):
    product = Product.objects.get(slug=slug) 
    customer = request.user
    cart = Cart.objects.get(customer=customer)

    try:
        cart_item = CartItem.objects.get(cart=cart,cart__customer=customer, product=product, is_active=True)
        cart_item.quantity += 1
        cart_item.save()


        dictionary_resp = {
            "quantity": cart_item.quantity,
            "total_price": cart_item.product.price * cart_item.quantity,
            "get_total_cart_price":CartItem.get_total_cart_price(cart)
        }
        return HttpResponse(json.dumps(dictionary_resp))
    except CartItem.DoesNotExist:
        pass

    return redirect('store_cart')



@login_required
def decrease_cart(request, slug):
    product = Product.objects.get(slug=slug) 
    customer = request.user
    cart = Cart.objects.get(customer=customer)

    try:
        cart_item = CartItem.objects.get(cart=cart,cart__customer=customer, product=product, is_active=True)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        dictionary_resp = {
            "quantity": cart_item.quantity,
            "total_price": cart_item.product.price * cart_item.quantity,
            "get_total_cart_price":CartItem.get_total_cart_price(cart)
        }
        return HttpResponse(json.dumps(dictionary_resp))
    except CartItem.DoesNotExist:
        pass

    return redirect('store_cart')



@login_required
def remove_from_cart(request,slug):
    product = Product.objects.get(slug=slug) 
    customer = request.user
    cart = Cart.objects.get(customer=customer)

    try:
        cart_item = CartItem.objects.get(cart=cart,cart__customer=customer, product=product, is_active=True)
        cart_item.delete()
        dictionary_resp = {
            "get_total_cart_price":CartItem.get_total_cart_price(cart)
        }
    except CartItem.DoesNotExist:
        pass

   
    return HttpResponse(json.dumps(dictionary_resp))



class StoreCart(LoginRequiredMixin, View):
    def get_cart_total(self, cart_items):
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_total_item_price()
        return total
    
    def get(self, request, *args, **kwargs):
        try:
            cart_items = CartItem.objects.filter(cart__customer=request.user, is_active=True)
            cart_total = self.get_cart_total(cart_items)
            customer = request.user.username
            context = {
                'cart_items': cart_items,
                'cart_total': "{:.2f}".format(cart_total),
                'customer':customer
            }
            return render(request, 'store_cart.html', context)
        except ObjectDoesNotExist:
            return redirect('store')
        

class OrderCheckout(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        form = OrderCheckoutForm()
        cart_items = CartItem.objects.filter(cart__customer=request.user, is_active=True)
        cart_total=0
        for cart_item in cart_items:
            cart_total += cart_item.get_total_item_price()
        customer = request.user.username
        context = {
            'form':form,
            'cart_total':cart_total,
            'customer':customer
        }
        return render(request,'order_checkout.html',context)
    

    def post(self, request, *args, **kwargs):
        form = OrderCheckoutForm(request.POST)
        cart_items = CartItem.objects.filter(cart__customer=request.user, is_active=True)
        cart_total = 0
        for cart_item in cart_items:
            cart_total += cart_item.get_total_item_price()

        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name'] 
            order.city = form.cleaned_data['city']
            order.address = form.cleaned_data['address']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.note = form.cleaned_data['note']
            order.customer=request.user
            order.is_ordered = True
            order.save()

            
            for cart_item in cart_items:
                order_product = OrderProduct()
                order_product.order = order
                order_product.quantity = cart_item.quantity
                order_product.save()
                order_product.products.set([cart_item.product])

            cart_items.delete()

        return redirect('store')



class Orders(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            orders = Order.objects.filter(customer=request.user).order_by('-created_at')
            context={
                'orders':orders
            }
            return render(request,'orders.html',context)
        except:
            pass


class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order_products = OrderProduct.objects.filter(order=order)
        context = {
            'order': order,
            'order_products':order_products
        }
        return render(request, 'order_detail.html', context)
    



        


   