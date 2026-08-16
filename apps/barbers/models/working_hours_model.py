from django.db import models
from barbers import models


class WorkingHoursModel(models.Model):
    DAYS_OF_WEEK = (
        (0, 'شنبه'),
        (1, 'یکشنبه'),
        (2, 'دوشنبه'),
        (3, 'سه‌شنبه'),
        (4, 'چهارشنبه'),
        (5, 'پنج‌شنبه'),
        (6, 'جمعه'),
    )

    barber = models.ForeignKey(
        models.BarberModel,
        on_delete=models.CASCADE,
        related_name='working_hours',
        verbose_name='آرایشگر',
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAYS_OF_WEEK, verbose_name='روز هفته'
    )
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    slot_duration = models.PositiveIntegerField(
        default=30, verbose_name='مدت زمان هر اسلات (دقیقه)'
    )
    is_closed = models.BooleanField(default=False, verbose_name='تعطیل است')

    class Meta:
        unique_together = ('barber', 'day_of_week')
        verbose_name = 'ساعت کاری'
        verbose_name_plural = 'ساعات کاری'

    def __str__(self):
        return f"{self.barber.user.username} - {self.get_day_of_week_display()}"