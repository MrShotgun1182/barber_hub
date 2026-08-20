from typing import Optional
from admin_panel.models.admin_panel_model import AdminPanelModel


def GetAdminProfileService(
    user_id: Optional[int] = None, profile_id: Optional[int] = None
) -> Optional[AdminPanelModel]:
    """
    دریافت پروفایل ادمین بر اساس شناسه کاربر (user_id) یا شناسه پروفایل (profile_id)
    """
    try:
        if profile_id:
            return AdminPanelModel.objects.select_related('user').get(
                id=profile_id
            )
        if user_id:
            return AdminPanelModel.objects.select_related('user').get(
                user_id=user_id
            )
        return None
    except AdminPanelModel.DoesNotExist:
        return None