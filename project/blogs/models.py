from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField(max_length=200,unique=True)
    category = models.ForeignKey(Category,null=True,on_delete=models.DO_NOTHING)
    description = RichTextField()
    image = models.ImageField(upload_to='blogs/%Y/%m/%d/',blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name