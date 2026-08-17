from datetime import date, time
from typing import Optional
from booking import models as booking_models
from barbers import models as barbers_models


def CheckSlotAvailabilityService(
    barber: barbers_models.BarberModel,
    appointment_date: date,
    start_time: time,
    end_time: time,
    exclude_appointment_id: Optional[int] = None,
) -> bool:
    """
    بررسی عدم تداخل زمانی اسلات انتخابی با نوبت‌های فعال آرایشگر در یک تاریخ
    """
    overlapping_appointments = booking_models.AppointmentModel.objects.filter(
        barber=barber,
        date=appointment_date,
        status__in=['PENDING', 'CONFIRMED'],
        start_time__lt=end_time,
        end_time__gt=start_time,
    )

    if exclude_appointment_id is not None:
        overlapping_appointments = overlapping_appointments.exclude(
            id=exclude_appointment_id
        )

    return not overlapping_appointments.exists()