from typing import Optional
from barbers import models


def UpdateBarberService(
    barber: models.BarberModel,
    bio: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> models.BarberModel:
    """
    بروزرسانی اطلاعات پروفایل آرایشگر
    """
    if bio is not None:
        barber.bio = bio
    if is_active is not None:
        barber.is_active = is_active

    barber.save()
    return barber