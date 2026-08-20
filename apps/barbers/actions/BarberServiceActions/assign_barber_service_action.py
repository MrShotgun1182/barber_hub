from datetime import time
from typing import Optional
from django.db import transaction
from barbers import models, services as barbers_services
from salon_services import models as salon_services_models

def AssignBarberServiceAction(
    barber: models.BarberModel,
    service: salon_services_models.ServiceModel,
    custom_price: Optional[int] = None,
    custom_duration_minutes: Optional[int] = None,
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
    is_active: bool = True,
) -> models.BarberServiceModel:
    """
    اختصاص یا به‌روزرسانی خدمت اختصاصی آرایشگر در یک تراکنش اتمیک
    """
    with transaction.atomic():
        barber_service = barbers_services.AddBarberServiceService(
            barber=barber,
            service=service,
            custom_price=custom_price,
            custom_duration_minutes=custom_duration_minutes,
            start_time=start_time,
            end_time=end_time,
            is_active=is_active,
        )
        return barber_service