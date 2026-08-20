from datetime import time
from django.db import transaction

from barbers import models, services as barbers_services


def SetBarberWorkingHoursAction(
    barber: models.BarberModel,
    day_of_week: int,
    start_time: time,
    end_time: time,
    slot_duration: int = 30,
    is_closed: bool = False,
) -> models.WorkingHoursModel:
    """
    تنظیم یا بروزرسانی ساعات کاری آرایشگر در یک تراکنش اتمیک
    """
    with transaction.atomic():
        working_hours = barbers_services.SetBarberWorkingHoursService(
            barber=barber,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            is_closed=is_closed,
        )
        return working_hours