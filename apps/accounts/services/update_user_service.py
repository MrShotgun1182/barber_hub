from typing import Optional
from accounts import models


def UpdateUserService(
    user: models.UserModel,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    role: Optional[str] = None,
) -> models.UserModel:
    """
    بروزرسانی اطلاعات کاربری
    """
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        user.email = email
    if phone_number is not None:
        user.phone_number = phone_number
    if role is not None:
        user.role = role

    user.save()
    return user