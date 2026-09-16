from django.contrib import admin
from customers import models as customers_models

@admin.register(customers_models.CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date')
    search_fields = ('user__username', 'user__phone_number')