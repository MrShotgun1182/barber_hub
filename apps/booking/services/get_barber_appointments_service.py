from datetime import date
from typing import Optional
from django.db.models import QuerySet
from booking import models as booking_models
from barbers import models as barbers_models


def GetBarberAppointmentsService(
    barber: barbers_models.BarberModel,
    appointment_date: Optional[date] = None,
    status: Optional[str] = None,
) -> QuerySet[booking_models.AppointmentModel]:
    """
    دریافت لیست نوبت‌های یک آرایشگر بر اساس تاریخ و وضعیت
    """
    queryset = booking_models.AppointmentModel.objects.filter(barber=barber)
    if appointment_date is not None:
        queryset = queryset.filter(date=appointment_date)
    if status is not None:
        queryset = queryset.filter(status=status)
    return queryset