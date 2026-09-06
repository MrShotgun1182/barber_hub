import datetime
from django.db import models
from django.utils import timezone


class OTPModel(models.Model):
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    code = models.CharField(max_length=6, verbose_name='کد تایید')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد'
    )
    is_used = models.BooleanField(default=False, verbose_name='مصرف شده')

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کدهای یکبار مصرف'
        ordering = ['-created_at']

    def is_valid(self, expiry_minutes=2) -> bool:
        """بررسی اعتبار زمانی کد (پیش‌فرض ۲ دقیقه)"""
        now = timezone.now()
        return not self.is_used and (
            now - self.created_at
        ) <= datetime.timedelta(minutes=expiry_minutes)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"