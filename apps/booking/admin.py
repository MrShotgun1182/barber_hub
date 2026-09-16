from django.contrib import admin
from booking import models as booking_models

@admin.register(booking_models.AppointmentModel)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'barber', 'date', 'start_time', 'end_time', 'total_price', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__user__username', 'barber__user__username', 'customer__user__phone_number')
    filter_horizontal = ('services',)