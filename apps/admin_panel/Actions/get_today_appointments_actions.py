from booking import services as booking_services


def GetTodayAppointmentsAction() -> dict:
    """
    ارکستراسیون دریافت داده‌های داشبورد مدیریت شامل لیست تمام نوبت‌های امروز
    """
    data = booking_services.GetTodayAppointmentsService()

    return {
        'today_appointments': data['today_appointments'],
        'today_appointments_count': data['today_appointments_count'],
        'error': None,
    }