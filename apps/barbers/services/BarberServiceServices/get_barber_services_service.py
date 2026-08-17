from django.db.models import QuerySet
from barbers import models


def GetBarberServicesService(
    barber: models.BarberModel,
    is_active_only: bool = True,
) -> QuerySet[models.BarberServiceModel]:
    """
    دریافت لیست خدمات ارائه شده توسط یک آرایشگر
    """
    queryset = models.BarberServiceModel.objects.filter(barber=barber)
    if is_active_only:
        queryset = queryset.filter(is_active=True)
    return queryset