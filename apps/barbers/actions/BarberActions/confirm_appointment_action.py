from django.db import transaction

from booking import models as booking_models, services as booking_services


def ConfirmAppointmentAction(
    appointment: booking_models.AppointmentModel,
) -> booking_models.AppointmentModel:
    """
    تایید نوبت رزروشده توسط آرایشگر در یک تراکنش اتمیک
    """
    with transaction.atomic():
        confirmed_appointment = booking_services.UpdateAppointmentStatusService(
            appointment=appointment,
            status='CONFIRMED',
        )
        return confirmed_appointment