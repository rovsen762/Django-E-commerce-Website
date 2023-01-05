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

class OrderProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def get_total_item_price(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey('CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.customer.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_item_price()
        return total

class CheckoutAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    note = models.TextField()

    def __str__(self):
        return self.customer.username