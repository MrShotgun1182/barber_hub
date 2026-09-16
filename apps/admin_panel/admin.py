from django.contrib import admin
from admin_panel import models as admin_panel_models

@admin.register(admin_panel_models.AdminPanelModel)
class AdminPanelAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    search_fields = ('user__username', 'title')