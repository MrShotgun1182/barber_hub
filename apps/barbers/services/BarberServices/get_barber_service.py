from typing import Optional
from barbers import models


def GetBarberService(
    user_id: Optional[int] = None, barber_id: Optional[int] = None
) -> Optional[models.BarberModel]:
    """
    دریافت اطلاعات آرایشگر بر اساس شناسه کاربر یا شناسه آرایشگر
    """
    try:
        if barber_id is not None:
            return models.BarberModel.objects.get(id=barber_id)
        if user_id is not None:
            return models.BarberModel.objects.get(user_id=user_id)
        return None
    except models.BarberModel.DoesNotExist:
        return None