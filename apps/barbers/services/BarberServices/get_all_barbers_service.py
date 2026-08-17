from django.db.models import QuerySet
from barbers import models


def GetAllBarbersService(
    is_active_only: bool = True,
) -> QuerySet[models.BarberModel]:
    """
    دریافت لیست آرایشگران (با امکان فیلتر بر اساس وضعیت فعالیت)
    """
    queryset = models.BarberModel.objects.all()
    if is_active_only:
        queryset = queryset.filter(is_active=True)
    return queryset