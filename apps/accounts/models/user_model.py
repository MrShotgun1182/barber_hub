from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    ROLE_CHOICES = (
        ('CUSTOMER', 'مشتری'),
        ('BARBER', 'آرایشگر'),
        ('MANAGER', 'مدیر'),
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        verbose_name='شماره موبایل',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER',
        verbose_name='نقش کاربر',
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"