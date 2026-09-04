from datetime import date
from booking import models as booking_models


def GetTodayAppointmentsService() -> dict:
    """
    دریافت تمام نوبت‌های امروز به همراه تعداد کل آن‌ها جهت نمایش در داشبورد مدیریت
    """
    today = date.today()
    today_appointments = (
        booking_models.AppointmentModel.objects.filter(date=today)
        .select_related('customer__user', 'barber__user', 'service')
        .order_by('start_time')
    )

    return {
        'today_appointments': today_appointments,
        'today_appointments_count': today_appointments.count(),
    }