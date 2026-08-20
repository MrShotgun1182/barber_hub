from datetime import date
from typing import Optional
from django.db import transaction
from accounts import services as accounts_services
from customers import models, services as customers_services


def RegisterCustomerAction(
    username: str,
    password: str,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    birth_date: Optional[date] = None,
) -> models.CustomerModel:
    """
    ثبت‌نام مشتری: ایجاد کاربر با نقش CUSTOMER و ایجاد پروفایل مشتری در یک تراکنش اتمیک
    """
    with transaction.atomic():
        user = accounts_services.CreateUserService(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role='CUSTOMER',
        )

        customer = customers_services.CreateCustomerService(
            user=user,
            birth_date=birth_date,
        )

        return customer