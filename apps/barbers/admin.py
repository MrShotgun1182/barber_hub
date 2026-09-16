from django.contrib import admin
from barbers import models as barbers_models

@admin.register(barbers_models.BarberModel)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__phone_number', 'bio')

@admin.register(barbers_models.BarberServiceModel)
class BarberServiceAdmin(admin.ModelAdmin):
    list_display = ('barber', 'service', 'custom_price', 'custom_duration_minutes', 'is_active')
    list_filter = ('is_active', 'service')
    search_fields = ('barber__user__username', 'service__name')

@admin.register(barbers_models.WorkingHoursModel)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('barber', 'day_of_week', 'start_time', 'end_time', 'slot_duration', 'is_closed')
    list_filter = ('day_of_week', 'is_closed')
    search_fields = ('barber__user__username',)