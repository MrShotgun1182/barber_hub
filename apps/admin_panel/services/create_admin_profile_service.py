from typing import Optional
from django.contrib.auth import get_user_model
from admin_panel.models.admin_panel_model import AdminPanelModel

User = get_user_model()


def CreateAdminProfileService(
    user_id: int, title: Optional[str] = None
) -> AdminPanelModel:
    """
    ایجاد پروفایل ادمین جدید برای کاربر مشخص‌شده
    """
    user = User.objects.get(id=user_id)
    admin_profile = AdminPanelModel.objects.create(
        user=user,
        title=title
    )
    return admin_profile