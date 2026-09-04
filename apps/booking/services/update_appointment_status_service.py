from typing import Any, Dict
from booking import models


def UpdateAppointmentStatusService(
    user: Any,
    appointment_id: int,
    status: str,
) -> Dict[str, Any]:
    """
    بررسی دسترسی دیتابیسی آرایشگر و تغییر وضعیت نوبت
    """
    valid_statuses = [choice[0] for choice in models.AppointmentModel.STATUS_CHOICES]
    if status not in valid_statuses:
        return {
            'success': False,
            'error': 'وضعیت ارسالی معتبر نیست.',
            'appointment': None,
        }

    try:
        appointment = models.AppointmentModel.objects.get(id=appointment_id)
    except models.AppointmentModel.DoesNotExist:
        return {
            'success': False,
            'error': 'نوبت مورد نظر یافت نشد.',
            'appointment': None,
        }

    barber_profile = getattr(user, 'barber_profile', None)
    if not barber_profile or appointment.barber != barber_profile:
        return {
            'success': False,
            'error': 'شما مجاز به تغییر وضعیت این نوبت نیستید.',
            'appointment': None,
        }

    appointment.status = status
    appointment.save()

    return {'success': True, 'error': None, 'appointment': appointment}