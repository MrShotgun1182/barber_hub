from salon_services import services as salon_services_services


def GetAllSalonServicesAction(is_active_only: bool = False) -> dict:
    """
    ارکستراسیون دریافت لیست خدمات سالن جهت مدیریت در پنل ادمین
    """
    services = salon_services_services.GetAllServicesService(
        is_active_only=is_active_only
    )

    return {
        'services': services,
    }