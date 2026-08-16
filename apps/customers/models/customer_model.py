from django.conf import settings
from django.db import models


class CustomerModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name='کاربر',
    )
    birth_date = models.DateField(
        null=True, blank=True, verbose_name='تاریخ تولد'
    )

    class Meta:
        verbose_name = 'پروفایل مشتری'
        verbose_name_plural = 'پروفایل‌های مشتریان'

    def __str__(self):
        return f"Customer: {self.user.username}"