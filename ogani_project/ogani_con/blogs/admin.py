from django.contrib import admin
from .models import Blog,Category
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['name','description','image','date','available']
    search_fields = ['name', 'description']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
