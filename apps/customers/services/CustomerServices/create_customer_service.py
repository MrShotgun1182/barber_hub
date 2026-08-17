from datetime import date
from typing import Optional, Any
from customers import models


def CreateCustomerService(
    user: Any, birth_date: Optional[date] = None
) -> models.CustomerModel:
    """
    ایجاد یا دریافت پروفایل مشتری و بروزرسانی اطلاعات آن
    """
    customer, created = models.CustomerModel.objects.get_or_create(
        user=user,
        defaults={'birth_date': birth_date}
    )
    
    if not created and birth_date is not None:
        customer.birth_date = birth_date
        customer.save()

    return customer