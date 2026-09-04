from typing import Dict, Any
from barbers.models.barber_model import BarberModel
from barbers import services as barbers_services
from salon_services import services as salon_service_services


def UpdateBarberServicesAction(barber: BarberModel, post_data: Dict[str, Any]) -> None:
    """
    پردازش فرم و به‌روزرسانی خدمات اختصاصی آرایشگر
    """
    selected_service_ids = post_data.getlist('selected_services')
    all_salon_services = salon_service_services.GetAllServicesService(is_active_only=True)

    for service in all_salon_services:
        if str(service.id) in selected_service_ids:
            custom_price_raw = post_data.get(f'price_{service.id}', '').strip()
            custom_duration_raw = post_data.get(f'duration_{service.id}', '').strip()

            custom_price = int(custom_price_raw) if custom_price_raw.isdigit() else None
            custom_duration = int(custom_duration_raw) if custom_duration_raw.isdigit() else None

            barbers_services.UpdateOrCreateBarberServiceService(
                barber_id=barber.id,
                service_id=service.id,
                custom_price=custom_price,
                custom_duration_minutes=custom_duration,
                is_active=True
            )
        else:
            barbers_services.UpdateOrCreateBarberServiceService(
                barber_id=barber.id,
                service_id=service.id,
                is_active=False
            )