import datetime
from django.db import models
from django.utils import timezone


class OTPModel(models.Model):
    # حداکثر تلاش ناموفق مجاز برای هر کد پیش از باطل شدن (مقابله با brute-force)
    MAX_ATTEMPTS = 5

    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    code = models.CharField(max_length=6, verbose_name='کد تایید')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد'
    )
    is_used = models.BooleanField(default=False, verbose_name='مصرف شده')
    attempts = models.PositiveSmallIntegerField(
        default=0, verbose_name='تعداد تلاش ناموفق'
    )

    @property
    def is_locked(self) -> bool:
        """آیا کد به سقف تلاش ناموفق رسیده و باطل شده است؟"""
        return self.is_used or self.attempts >= self.MAX_ATTEMPTS

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