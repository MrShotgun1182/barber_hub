from accounts import services


def AdminAuthenticateAction(username: str, password: str) -> bool:
    """
    اعتبارسنجی و بررسی صحت نقش مدیر سیستم و فعال بودن حساب کاربر
    """
    user = services.AuthenticateUserService(username=username, password=password)

    if user and user.role == 'MANAGER':
        manager_profile = getattr(user, 'manager_profile', None)
        if manager_profile and user.is_active:
            return True

    return False