from django.contrib import admin
from .models import Contact
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message')
    list_filter = ('name', 'email', 'phone', 'message')
    search_fields = ('name', 'email', 'phone', 'message')
    list_per_page = 10