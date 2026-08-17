from typing import Optional
from customers import models


def GetCustomerService(
    user_id: Optional[int] = None, customer_id: Optional[int] = None
) -> Optional[models.CustomerModel]:
    """
    دریافت پروفایل مشتری بر اساس شناسه کاربر یا شناسه مشتری
    """
    try:
        if customer_id is not None:
            return models.CustomerModel.objects.get(id=customer_id)
        if user_id is not None:
            return models.CustomerModel.objects.get(user_id=user_id)
        return None
    except models.CustomerModel.DoesNotExist:
        return None