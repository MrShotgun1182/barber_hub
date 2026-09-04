from typing import Any, Dict
from django.utils import timezone

from booking import services as booking_services


def GetBarberTodayAppointmentsAction(user: Any) -> Dict[str, Any]:
    """
    دریافت تمام نوبت‌های امروز آرایشگر (تا پایان شب) از طریق لایه سرویس
    """
    barber = getattr(user, 'barber_profile', None)
    if not barber:
        return {
            'success': False,
            'error': 'پروفایل آرایشگر برای این کاربر یافت نشد.',
            'appointments': [],
            'count': 0,
        }

    today = timezone.now().date()

    appointments = booking_services.GetBarberAppointmentsService(
        barber=barber,
        appointment_date=today,
    )

    return {
        'success': True,
        'error': None,
        'appointments': appointments,
        'count': appointments.count(),
    }