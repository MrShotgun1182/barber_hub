from django.db import models
from barbers.models import BarberModel
from salon_services import models


class BarberServiceModel(models.Model):
    barber = models.ForeignKey(
        BarberModel,
        on_delete=models.CASCADE,
        related_name='barber_services',
        verbose_name='آرایشگر',
    )
    service = models.ForeignKey(
        models.ServiceModel,
        on_delete=models.CASCADE,
        related_name='barber_services',
        verbose_name='خدمت',
    )
    custom_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='قیمت اختصاصی (تومان)',
        help_text='در صورت خالی بودن، قیمت پایه خدمت اعمال می‌شود.',
    )
    custom_duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='مدت زمان اختصاصی (دقیقه)',
        help_text='در صورت خالی بودن، مدت زمان پیش‌فرض اعمال می‌شود.',
    )
    start_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='ساعت شروع ارائه خدمت',
        help_text='در صورت خالی بودن، تابع ساعات کاری عمومی آرایشگر است.',
    )
    end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='ساعت پایان ارائه خدمت',
        help_text='در صورت خالی بودن، تابع ساعات کاری عمومی آرایشگر است.',
    )
    is_active = models.BooleanField(default=True, verbose_name='وضعیت ارائه')

    class Meta:
        unique_together = ('barber', 'service')
        verbose_name = 'خدمت آرایشگر'
        verbose_name_plural = 'خدمات آرایشگران'

    def __str__(self):
        price = self.custom_price or self.service.base_price
        return f"{self.barber.user.username} - {self.service.name} ({price:,} تومان)"