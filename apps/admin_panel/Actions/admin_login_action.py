from django.contrib.auth import login
from accounts import services as accounts_services


def AdminLoginAction(request, username: str, password: str) -> dict:
    """
    ارکستراسیون احراز هویت، بررسی دسترسی مدیریتی، فعال بودن حساب و ورود کاربر
    """
    user = accounts_services.AuthenticateUserService(
        username=username, password=password
    )

    if user and (user.role == 'MANAGER' or user.is_staff or user.is_superuser):
        if user.is_active:
            login(request, user)
            return {'success': True, 'error': None}
        return {
            'success': False,
            'error': 'حساب کاربری مدیریتی شما غیرفعال است.',
        }

    return {
        'success': False,
        'error': 'نام کاربری یا رمز عبور اشتباه است یا دسترسی مدیریتی ندارید.',
    }