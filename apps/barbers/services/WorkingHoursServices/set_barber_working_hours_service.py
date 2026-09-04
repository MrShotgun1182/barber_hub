from typing import List, Dict, Any
from django.db import transaction
from barbers import models as barbers_models


def SetBarberWorkingHoursService(
    barber: barbers_models.BarberModel,
    day_of_week: int,
    shifts: List[Dict[str, Any]],
    is_closed: bool = False,
) -> List[barbers_models.WorkingHoursModel]:
    """
    حذف شیفت‌های قبلی روز مشخص‌شده و ثبت شیفت‌های جدید برای آن روز
    """
    with transaction.atomic():
        barbers_models.WorkingHoursModel.objects.filter(
            barber=barber, day_of_week=day_of_week
        ).delete()

        if is_closed:
            return []

        created_shifts = []
        for shift in shifts:
            wh = barbers_models.WorkingHoursModel.objects.create(
                barber=barber,
                day_of_week=day_of_week,
                start_time=shift['start_time'],
                end_time=shift['end_time'],
                slot_duration=shift.get('slot_duration', 30),
                is_closed=False,
            )
            created_shifts.append(wh)

        return created_shifts