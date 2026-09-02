from django.contrib.auth import login
from accounts import services as accounts_services


def BarberLoginAction(request, username: str, password: str) -> dict:
    """
    ارکستراسیون احراز هویت، بررسی نقش آرایشگر، فعال بودن حساب و ورود کاربر
    """
    user = accounts_services.AuthenticateUserService(
        username=username, password=password
    )

    if user and user.role == 'BARBER':
        barber_profile = getattr(user, 'barber_profile', None)
        if barber_profile and barber_profile.is_active:
            login(request, user)
            return {'success': True, 'error': None}
        return {
            'success': False,
            'error': 'پروفایل آرایشگری شما غیرفعال است.',
        }

    return {
        'success': False,
        'error': 'نام کاربری یا رمز عبور اشتباه است یا دسترسی آرایشگر ندارید.',
    }