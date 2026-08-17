from typing import Optional
from accounts import models


def CreateUserService(
    username: str,
    password: str,
    phone_number: Optional[str] = None,
    role: str = 'CUSTOMER',
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> models.UserModel:
    """
    ایجاد کاربر جدید در سیستم همراه با تنظیم نقش و هش رمز عبور
    """
    user = models.UserModel.objects.create_user(
        username=username,
        password=password,
        phone_number=phone_number,
        role=role,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user