from booking import models


def UpdateAppointmentStatusService(
    appointment: models.AppointmentModel,
    status: str,
) -> models.AppointmentModel:
    """
    بروزرسانی وضعیت نوبت رزرو شده
    """
    appointment.status = status
    appointment.save()
    return appointment