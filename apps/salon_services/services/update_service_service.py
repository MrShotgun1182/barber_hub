from typing import Optional
from salon_services import models


def UpdateServiceService(
    service: models.ServiceModel,
    name: Optional[str] = None,
    description: Optional[str] = None,
    base_price: Optional[int] = None,
    default_duration_minutes: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> models.ServiceModel:
    """
    بروزرسانی اطلاعات خدمت
    """
    if name is not None:
        service.name = name
    if description is not None:
        service.description = description
    if base_price is not None:
        service.base_price = base_price
    if default_duration_minutes is not None:
        service.default_duration_minutes = default_duration_minutes
    if is_active is not None:
        service.is_active = is_active

    service.save()
    return service