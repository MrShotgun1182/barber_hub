from typing import Optional
from django.db import transaction

from salon_services import (
    models as salon_services_models,
    services as salon_services_services,
)


def UpdateSalonServiceAction(
    service: salon_services_models.ServiceModel,
    name: Optional[str] = None,
    description: Optional[str] = None,
    base_price: Optional[int] = None,
    default_duration_minutes: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> salon_services_models.ServiceModel:
    """
    بروزرسانی مشخصات خدمت سالن در یک تراکنش اتمیک
    """
    with transaction.atomic():
        updated_service = salon_services_services.UpdateServiceService(
            service=service,
            name=name,
            description=description,
            base_price=base_price,
            default_duration_minutes=default_duration_minutes,
            is_active=is_active,
        )
        return updated_service