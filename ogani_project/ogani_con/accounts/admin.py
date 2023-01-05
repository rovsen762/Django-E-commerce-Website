from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Customer


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone',)}),
    )
    list_filter = ('phone',)

admin.site.register(Customer, CustomUserAdmin)
