from django.db import models


class ServiceModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام خدمت')
    description = models.TextField(
        blank=True, null=True, verbose_name='توضیحات'
    )
    base_price = models.PositiveIntegerField(
        verbose_name='قیمت پایه (تومان)'
    )
    default_duration_minutes = models.PositiveIntegerField(
        default=45, verbose_name='مدت زمان پیش‌فرض (دقیقه)'
    )
    is_active = models.BooleanField(default=True, verbose_name='وضعیت فعال')

    class Meta:
        verbose_name = 'خدمت سالن'
        verbose_name_plural = 'خدمات سالن'

    def __str__(self):
        return f"{self.name} - قیمت پایه: {self.base_price:,} تومان"