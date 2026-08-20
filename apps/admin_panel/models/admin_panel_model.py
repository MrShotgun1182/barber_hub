from django.conf import settings
from django.db import models


class AdminPanelModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='manager_profile',
        verbose_name='کاربر',
    )
    title = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='عنوان سمت'
    )

    class Meta:
        verbose_name = 'پروفایل مدیر'
        verbose_name_plural = 'پروفایل‌های مدیران'

    def __str__(self):
        return f"Manager: {self.user.username}"