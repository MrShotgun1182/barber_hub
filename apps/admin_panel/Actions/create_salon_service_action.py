from typing import Optional
from django.db import transaction

from salon_services import models as salon_services_models, services as salon_services_services


def CreateSalonServiceAction(
    name: str,
    base_price: int,
    description: Optional[str] = None,
    default_duration_minutes: int = 45,
    is_active: bool = True,
) -> salon_services_models.ServiceModel:
    """
    ایجاد و ثبت خدمت جدید سالن در یک تراکنش اتمیک
    """
    with transaction.atomic():
        service = salon_services_services.CreateServiceService(
            name=name,
            base_price=base_price,
            description=description,
            default_duration_minutes=default_duration_minutes,
            is_active=is_active,
        )
        return service