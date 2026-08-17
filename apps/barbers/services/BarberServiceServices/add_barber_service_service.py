from datetime import time
from typing import Any, Optional
from barbers import models


def AddBarberServiceService(
    barber: models.BarberModel,
    service: Any,
    custom_price: Optional[int] = None,
    custom_duration_minutes: Optional[int] = None,
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
    is_active: bool = True,
) -> models.BarberServiceModel:
    """
    اختصاص یا بروزرسانی خدمت اختصاصی برای آرایشگر
    """
    barber_service, _ = models.BarberServiceModel.objects.update_or_create(
        barber=barber,
        service=service,
        defaults={
            'custom_price': custom_price,
            'custom_duration_minutes': custom_duration_minutes,
            'start_time': start_time,
            'end_time': end_time,
            'is_active': is_active,
        },
    )
    return barber_service