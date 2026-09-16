from barbers import models as barbers_models


def GetBookingSummaryService(barber_id: int, barber_service_ids: list[int]) -> dict:
    """
    محاسبه و استخراج اطلاعات خلاصه فاکتور رزرو شامل نام آرایشگر،
    خدمات انتخابی، قیمت‌ها و مدت‌زمان‌ها
    """
    # ۱. دریافت اطلاعات آرایشگر
    try:
        barber = barbers_models.BarberModel.objects.select_related('user').get(
            id=barber_id, is_active=True
        )
    except barbers_models.BarberModel.DoesNotExist:
        raise ValueError('آرایشگر مورد نظر یافت نشد.')

    # ۲. دریافت خدمات انتخاب‌شده آرایشگر
    barber_services = barbers_models.BarberServiceModel.objects.filter(
        id__in=barber_service_ids,
        barber_id=barber_id,
        is_active=True,
        service__is_active=True
    ).select_related('service')

    if not barber_services.exists():
        raise ValueError('هیچ خدمت معتبری انتخاب نشده است.')

    services_data = []
    total_price = 0
    total_duration = 0

    # ۳. محاسبه قیمت و زمان هر خدمت (با در نظر گرفتن مقادیر اختصاصی)
    for bs in barber_services:
        service = bs.service
        
        effective_price = (
            bs.custom_price 
            if bs.custom_price is not None 
            else service.base_price
        )
        
        effective_duration = (
            bs.custom_duration_minutes 
            if bs.custom_duration_minutes is not None 
            else service.default_duration_minutes
        )

        total_price += effective_price
        total_duration += effective_duration

        services_data.append({
            'service_id': service.id,
            'barber_service_id': bs.id,
            'name': service.name,
            'price': effective_price,
            'duration_minutes': effective_duration,
        })

    barber_name = barber.user.get_full_name() or barber.user.username

    return {
        'barber_name': barber_name,
        'services': services_data,
        'total_price': total_price,
        'total_duration_minutes': total_duration,
    }