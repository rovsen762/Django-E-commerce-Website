from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,Category,OrderProduct,Order,CheckoutAddress
from blogs.models import Blog
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Customer
from .forms import CheckoutAddressForm


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



class StoreCart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'store_cart.html', context)
        except ObjectDoesNotExist:
            return redirect("store")



@login_required
def add_to_cart(request, slug): 
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        customer=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This item quantity was updated.")
            return render(request,"product.html",{'product':product})
        else:
            order.products.add(order_product)
            messages.info(request, "This item was added to your cart.")
            return render(request,"product.html",{'product':product})
    else:
        
        order = Order.objects.create(customer=request.user)
        order.products.add(order_product)
        messages.info(request, "This item was added to your cart.")
        return render(request,"product.html",{'product':product})


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                customer=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            order_product.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("store_cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('store_cart', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store_cart", slug=slug)


class StoreCheckout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutAddressForm()
        order = Order.objects.get(customer=self.request.user, ordered=False)
        context = {
            'form': form,
            'object': order
        }
        return render(self.request, 'store_checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutAddressForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                city = form.cleaned_data.get('city')
                address = form.cleaned_data.get('address')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                note = form.cleaned_data.get('note')

                checkout_address = CheckoutAddress(
                    customer=self.request.user,
                    first_name=first_name,
                    last_name=last_name,
                    city=city,
                    address=address,
                    phone=phone,
                    email=email,
                    note=note
                )
                checkout_address.save()
                order.address = checkout_address
                order.save()
                messages.success(self.request, "Your order was successful!")
                return redirect("store_checkout")
            messages.warning(self.request, "Failed checkout")
            return redirect("store_checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("store_checkout")




