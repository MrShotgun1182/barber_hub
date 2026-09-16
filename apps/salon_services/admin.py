from django.contrib import admin
from salon_services import models as salon_service_models

@admin.register(salon_service_models.ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'default_duration_minutes', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')