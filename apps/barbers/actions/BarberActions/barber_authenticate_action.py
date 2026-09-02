from accounts import services


def BarberAuthenticateAction(username: str, password: str) -> bool:
    """
    احراز هویت کاربر و بررسی صحت نقش آرایشگر و فعال بودن پروفایل
    """
    user = services.AuthenticateUserService(username=username, password=password)

    if user and user.role == 'BARBER':
        barber_profile = getattr(user, 'barber_profile', None)
        if barber_profile and barber_profile.is_active:
            return True

    return False