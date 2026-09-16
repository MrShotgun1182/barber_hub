from django.contrib import admin
from OTP import models as otp_models

@admin.register(otp_models.OTPModel)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone_number', 'code')