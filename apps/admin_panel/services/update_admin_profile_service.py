from typing import Optional
from admin_panel.models.admin_panel_model import AdminPanelModel


def UpdateAdminProfileService(
    profile_id: int, title: Optional[str] = None
) -> Optional[AdminPanelModel]:
    """
    بروزرسانی اطلاعات پروفایل ادمین
    """
    try:
        admin_profile = AdminPanelModel.objects.get(id=profile_id)
        if title is not None:
            admin_profile.title = title
        admin_profile.save()
        return admin_profile
    except AdminPanelModel.DoesNotExist:
        return None