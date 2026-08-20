from typing import Optional
from django.db import transaction

from accounts import services as accounts_services
from admin_panel import models, services as admin_panel_services


def RegisterManagerAction(
    username: str,
    password: str,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    title: Optional[str] = None,
) -> models.AdminPanelModel:
    """
    ثبت‌نام مدیر: ایجاد کاربر با نقش MANAGER و ساخت پروفایل مدیر در یک تراکنش اتمیک
    """
    with transaction.atomic():
        user = accounts_services.CreateUserService(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role='MANAGER',
        )

        manager = admin_panel_services.CreateAdminProfileService(
            user_id=user.id,
            title=title,
        )

        return manager