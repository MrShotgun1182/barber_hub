from datetime import date
from typing import Optional
from django.db import transaction
from accounts import services as accounts_services
from customers import models, services as customers_services

def UpdateCustomerProfileAction(
    customer: models.CustomerModel,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    birth_date: Optional[date] = None,
) -> models.CustomerModel:
    """
    بروزرسانی همزمان پروفایل مشتری و اطلاعات کاربری مرتبط در یک تراکنش اتمیک
    """
    with transaction.atomic():
        if any(arg is not None for arg in (first_name, last_name, email, phone_number)):
            accounts_services.UpdateUserService(
                user=customer.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )

        if birth_date is not None:
            customers_services.UpdateCustomerService(
                customer=customer,
                birth_date=birth_date,
            )

        customer.refresh_from_db()
        return customer