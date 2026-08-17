from typing import Optional
from django.contrib.auth import authenticate
from accounts import models


def AuthenticateUserService(
    username: str, password: str
) -> Optional[models.UserModel]:
    """
    اعتبارسنجی و بررسی صحت اطلاعات ورود کاربر
    """
    user = authenticate(username=username, password=password)
    if user is not None and isinstance(user, models.UserModel):
        return user
    return None