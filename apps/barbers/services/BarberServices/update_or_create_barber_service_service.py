from barbers.models.barber_service_model import BarberServiceModel

def UpdateOrCreateBarberServiceService(
    barber_id: int,
    service_id: int,
    custom_price: int = None,
    custom_duration_minutes: int = None,
    is_active: bool = True
) -> BarberServiceModel:
    """
    ایجاد یا به‌روزرسانی قیمت و زمان اختصاصی خدمت برای آرایشگر
    """
    barber_service, _ = BarberServiceModel.objects.update_or_create(
        barber_id=barber_id,
        service_id=service_id,
        defaults={
            'custom_price': custom_price if custom_price else None,
            'custom_duration_minutes': custom_duration_minutes if custom_duration_minutes else None,
            'is_active': is_active,
        }
    )
    return barber_service