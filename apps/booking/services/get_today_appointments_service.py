from django.utils import timezone
from booking import models as booking_models


def GetTodayAppointmentsService() -> dict:
    """
    دریافت تمام نوبت‌های امروز به همراه تعداد کل آن‌ها جهت نمایش در داشبورد مدیریت
    """
    # استفاده از timezone.now() برای هم‌خوانی با TIME_ZONE پروژه (Asia/Tehran)
    today = timezone.localdate()
    today_appointments = (
        booking_models.AppointmentModel.objects.filter(date=today)
        .select_related('customer__user', 'barber__user')
        .prefetch_related('services__service')
        .order_by('start_time')
    )

    return {
        'today_appointments': today_appointments,
        'today_appointments_count': today_appointments.count(),
    }