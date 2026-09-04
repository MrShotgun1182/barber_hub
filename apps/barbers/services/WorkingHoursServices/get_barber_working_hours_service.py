from django.db.models import QuerySet
from barbers import models as barbers_models


def GetBarberWorkingHoursService(
    barber: barbers_models.BarberModel,
) -> QuerySet[barbers_models.WorkingHoursModel]:
    """
    دریافت تمام شیفت‌های کاری ثبت‌شده آرایشگر به ترتیب روز و ساعت شروع
    """
    return barbers_models.WorkingHoursModel.objects.filter(
        barber=barber
    ).order_by('day_of_week', 'start_time')