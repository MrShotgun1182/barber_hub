from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts import models as accounts_models

@admin.register(accounts_models.UserModel)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'phone_number', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'phone_number', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی', {'fields': ('phone_number', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات تکمیلی', {'fields': ('phone_number', 'role')}),
    )