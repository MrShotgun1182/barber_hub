from typing import Optional
from booking import models


def GetAppointmentService(
    appointment_id: int,
) -> Optional[models.AppointmentModel]:
    """
    دریافت اطلاعات یک نوبت بر اساس شناسه
    """
    try:
        return models.AppointmentModel.objects.get(id=appointment_id)
    except models.AppointmentModel.DoesNotExist:
        return None