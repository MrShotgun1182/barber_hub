from typing import Optional
from accounts import models


def GetUserService(user_id: int) -> Optional[models.UserModel]:
    """
    دریافت اطلاعات کاربر بر اساس شناسه کاربری
    """
    try:
        return models.UserModel.objects.get(id=user_id)
    except models.UserModel.DoesNotExist:
        return None