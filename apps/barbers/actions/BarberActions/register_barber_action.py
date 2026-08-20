from typing import Optional
from django.db import transaction

from accounts import services as accounts_services
from barbers import models, services as barbers_services


def RegisterBarberAction(
    username: str,
    password: str,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    bio: Optional[str] = None,
    is_active: bool = True,
) -> models.BarberModel:
    """
    ثبت‌نام آرایشگر: ایجاد کاربر با نقش BARBER و ایجاد پروفایل آرایشگر در یک تراکنش اتمیک
    """
    with transaction.atomic():
        user = accounts_services.CreateUserService(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role='BARBER',
        )

        barber = barbers_services.CreateBarberService(
            user=user,
            bio=bio,
            is_active=is_active,
        )

        return barber