from typing import Optional
from django.db import transaction

from accounts import services as accounts_services
from barbers import models, services as barbers_services


def UpdateBarberProfileAction(
    barber: models.BarberModel,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    bio: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> models.BarberModel:
    """
    بروزرسانی همزمان پروفایل آرایشگر و اطلاعات کاربری مرتبط در یک تراکنش اتمیک
    """
    with transaction.atomic():
        if any(arg is not None for arg in (first_name, last_name, email, phone_number)):
            accounts_services.UpdateUserService(
                user=barber.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )

        if bio is not None or is_active is not None:
            barbers_services.UpdateBarberService(
                barber=barber,
                bio=bio,
                is_active=is_active,
            )

        barber.refresh_from_db()
        return barber