from typing import Optional
from salon_services import models


def CreateServiceService(
    name: str,
    base_price: int,
    description: Optional[str] = None,
    default_duration_minutes: int = 45,
    is_active: bool = True,
) -> models.ServiceModel:
    """
    ایجاد و ثبت خدمت جدید در سالن
    """
    return models.ServiceModel.objects.create(
        name=name,
        base_price=base_price,
        description=description,
        default_duration_minutes=default_duration_minutes,
        is_active=is_active,
    )