from admin_panel.models.admin_panel_model import AdminPanelModel


def DeleteAdminProfileService(profile_id: int) -> bool:
    """
    حذف پروفایل ادمین بر اساس شناسه
    """
    try:
        admin_profile = AdminPanelModel.objects.get(id=profile_id)
        admin_profile.delete()
        return True
    except AdminPanelModel.DoesNotExist:
        return False