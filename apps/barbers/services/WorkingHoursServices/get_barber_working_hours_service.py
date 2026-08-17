from django.db.models import QuerySet
from barbers import models


def GetBarberWorkingHoursService(
    barber: models.BarberModel,
) -> QuerySet[models.WorkingHoursModel]:
    """
    دریافت برنامه و ساعات کاری یک آرایشگر
    """
    return models.WorkingHoursModel.objects.filter(barber=barber).order_by(
        'day_of_week'
    )