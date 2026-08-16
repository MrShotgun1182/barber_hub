from django.conf import settings
from django.db import models


class BarberModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='barber_profile',
        verbose_name='کاربر',
    )
    bio = models.TextField(
        blank=True, null=True, verbose_name='درباره آرایشگر'
    )
    is_active = models.BooleanField(
        default=True, verbose_name='وضعیت فعالیت'
    )

    class Meta:
        verbose_name = 'پروفایل آرایشگر'
        verbose_name_plural = 'پروفایل‌های آرایشگران'

    def __str__(self):
        return f"Barber: {self.user.username}"