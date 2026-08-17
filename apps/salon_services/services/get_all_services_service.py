from django.db.models import QuerySet
from salon_services import models


def GetAllServicesService(
    is_active_only: bool = True,
) -> QuerySet[models.ServiceModel]:
    """
    دریافت لیست خدمات سالن (با امکان فیلتر بر اساس خدمات فعال)
    """
    queryset = models.ServiceModel.objects.all()
    if is_active_only:
        queryset = queryset.filter(is_active=True)
    return queryset