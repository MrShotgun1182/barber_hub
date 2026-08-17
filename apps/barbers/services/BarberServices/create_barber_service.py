from typing import Optional, Any
from barbers import models


def CreateBarberService(
    user: Any,
    bio: Optional[str] = None,
    is_active: bool = True,
) -> models.BarberModel:
    """
    ایجاد یا دریافت و بروزرسانی پروفایل آرایشگر
    """
    barber, created = models.BarberModel.objects.get_or_create(
        user=user,
        defaults={
            'bio': bio,
            'is_active': is_active,
        },
    )

    if not created:
        if bio is not None:
            barber.bio = bio
        barber.is_active = is_active
        barber.save()

    return barber