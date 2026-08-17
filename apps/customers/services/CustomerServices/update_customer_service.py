from datetime import date
from typing import Optional
from customers import models


def UpdateCustomerService(
    customer: models.CustomerModel,
    birth_date: Optional[date] = None,
) -> models.CustomerModel:
    """
    بروزرسانی اطلاعات پروفایل مشتری
    """
    if birth_date is not None:
        customer.birth_date = birth_date
        customer.save()

    return customer