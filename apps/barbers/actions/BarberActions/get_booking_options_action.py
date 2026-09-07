from barbers import services


def GetBookingOptionsAction() -> dict:
    """
    اکشن دریافت و بسته‌بندی گزینه‌های رزرو برای فرانت‌اند
    """
    barbers_list = services.GetBarbersWithServicesService()

    return {
        'status': 'success',
        'count': len(barbers_list),
        'barbers': barbers_list
    }