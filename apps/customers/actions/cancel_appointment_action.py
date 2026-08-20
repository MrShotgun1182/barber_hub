from django.db import transaction
from booking import models as booking_models, services as booking_services

def CancelAppointmentAction(
    appointment: booking_models.AppointmentModel,
) -> booking_models.AppointmentModel:
    """
    لغو نوبت رزروشده برای مشتری در یک تراکنش اتمیک
    """
    with transaction.atomic():
        canceled_appointment = booking_services.UpdateAppointmentStatusService(
            appointment=appointment,
            status='CANCELLED',
        )
        return canceled_appointment