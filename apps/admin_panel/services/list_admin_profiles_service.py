from typing import Optional
from django.db.models import QuerySet
from admin_panel.models.admin_panel_model import AdminPanelModel

def ListAdminProfilesService(
    title_search: Optional[str] = None,
) -> QuerySet[AdminPanelModel]:
    """
    دریافت لیست پروفایل‌های ادمین با قابلیت جستجو بر اساس عنوان سمت
    """
    queryset = AdminPanelModel.objects.select_related('user').all()
    if title_search:
        queryset = queryset.filter(title__icontains=title_search)
    return queryset