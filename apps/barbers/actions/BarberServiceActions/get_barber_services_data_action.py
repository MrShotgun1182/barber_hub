from typing import List, Dict, Any
from barbers.models.barber_model import BarberModel
from barbers import services as barber_services
from salon_services import services as salon_service_services


def GetBarberServicesDataAction(barber: BarberModel) -> List[Dict[str, Any]]:
    """
    آماده‌سازی لیست خدمات سالن همراه با تنظیمات اختصاصی آرایشگر
    """
    salon_services = salon_service_services.GetAllServicesService(is_active_only=True)
    existing_barber_services = barber_services.GetBarberServicesService(barber=barber, is_active_only=False)

    barber_services_map = {bs.service_id: bs for bs in existing_barber_services}

    services_data = []
    for service in salon_services:
        barber_service = barber_services_map.get(service.id)
        services_data.append({
            'service': service,
            'is_selected': barber_service.is_active if barber_service else False,
            'custom_price': barber_service.custom_price if barber_service else None,
            'custom_duration_minutes': barber_service.custom_duration_minutes if barber_service else None,
        })

    return services_data