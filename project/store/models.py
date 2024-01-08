from django.db import models
from accounts.models import Customer
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    price = models.FloatField()
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    information = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'category_slug': self.category.slug, 'product_id': self.id})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug})



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

 
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    def get_total_item_price(self):
        return round(self.product.price * self.quantity,3)
    

    @staticmethod 
    def get_total_cart_price(cart):
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total_price = sum(item.get_total_item_price() for item in cart_items)
        return round(total_price,3)
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    note = models.TextField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username


    def get_total_order_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum(item.get_total_item_price() for item in order_products)
        return total_price
    
    def get_total_products_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum(item.quantity for item in order_products)
        return total_quantity
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    def get_total_item_price(self):
        total_price = 0
        for product in self.products.all():
            total_price += product.price * self.quantity
        return total_price
    
    
    
