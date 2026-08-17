from datetime import time
from barbers import models


def SetBarberWorkingHoursService(
    barber: models.BarberModel,
    day_of_week: int,
    start_time: time,
    end_time: time,
    slot_duration: int = 30,
    is_closed: bool = False,
) -> models.WorkingHoursModel:
    """
    ثبت یا بروزرسانی ساعت کاری روزانه برای یک آرایشگر
    """
    working_hours, _ = models.WorkingHoursModel.objects.update_or_create(
        barber=barber,
        day_of_week=day_of_week,
        defaults={
            'start_time': start_time,
            'end_time': end_time,
            'slot_duration': slot_duration,
            'is_closed': is_closed,
        },
    )
    return working_hours