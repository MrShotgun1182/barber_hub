from accounts import models


def ChangeUserPasswordService(
    user: models.UserModel, new_password: str
) -> models.UserModel:
    """
    تغییر و بروزرسانی امن رمز عبور کاربر
    """
    user.set_password(new_password)
    user.save()
    return user