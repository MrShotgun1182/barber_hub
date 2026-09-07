from django.db import models
from barbers import models as barbers_models
from customers import models as customers_models


class AppointmentModel(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'در انتظار تایید'),
        ('CONFIRMED', 'تایید شده'),
        ('COMPLETED', 'انجام شده'),
        ('CANCELLED', 'لغو شده'),
    )

    customer = models.ForeignKey(
        customers_models.CustomerModel,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='مشتری',
    )
    barber = models.ForeignKey(
        barbers_models.BarberModel,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='آرایشگر',
    )
    # اتصال چندبه‌چند به خدمات اختصاصی آرایشگر
    services = models.ManyToManyField(
        barbers_models.BarberServiceModel,
        related_name='appointments',
        verbose_name='خدمات انتخاب‌شده',
    )
    date = models.DateField(verbose_name='تاریخ نوبت')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    total_price = models.PositiveIntegerField(
        default=0, verbose_name='مجموع قیمت ثبت‌شده (تومان)'
    )
    total_duration_minutes = models.PositiveIntegerField(
        default=0, verbose_name='مجموع مدت زمان (دقیقه)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='وضعیت نوبت',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ثبت'
    )

    class Meta:
        verbose_name = 'رزرو نوبت'
        verbose_name_plural = 'رزروهای نوبت'
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.customer.user.username} - {self.barber.user.username} - {self.date} {self.start_time}"