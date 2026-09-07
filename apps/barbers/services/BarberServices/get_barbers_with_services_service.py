from barbers.models.barber_model import BarberModel


def GetBarbersWithServicesService() -> list[dict]:
    """
    استخراج لیست تمام آرایشگران فعال به همراه خدمات فعال آن‌ها
    و محاسبه قیمت و مدت زمان نهایی (ترجیح مقادیر اختصاصی آرایشگر بر مقادیر پایه)
    """
    # کوئری بهینه به همراه select_related و prefetch_related برای جلوگیری از مشکل N+1 Query
    barbers = BarberModel.objects.filter(is_active=True).select_related('user').prefetch_related(
        'barber_services__service'
    )

    barbers_data = []

    for barber in barbers:
        services_list = []
        
        # پیمایش خدمات فعال این آرایشگر
        for barber_service in barber.barber_services.filter(is_active=True, service__is_active=True):
            service = barber_service.service
            
            # منطق انتخاب قیمت و زمان (اگر مقدار اختصاصی وجود داشت، همان؛ وگرنه مقدار پایه)
            effective_price = (
                barber_service.custom_price 
                if barber_service.custom_price is not None 
                else service.base_price
            )
            
            effective_duration = (
                barber_service.custom_duration_minutes 
                if barber_service.custom_duration_minutes is not None 
                else service.default_duration_minutes
            )

            services_list.append({
                'barber_service_id': barber_service.id,
                'service_id': service.id,
                'name': service.name,
                'description': service.description or '',
                'price': effective_price,
                'duration_minutes': effective_duration,
                'start_time': barber_service.start_time.strftime('%H:%M') if barber_service.start_time else None,
                'end_time': barber_service.end_time.strftime('%H:%M') if barber_service.end_time else None,
            })

        # نام کامل کاربر یا نام کاربری در صورت خالی بودن
        full_name = barber.user.get_full_name() or barber.user.username

        barbers_data.append({
            'barber_id': barber.id,
            'name': full_name,
            'username': barber.user.username,
            'bio': barber.bio or '',
            'services': services_list
        })

    return barbers_data