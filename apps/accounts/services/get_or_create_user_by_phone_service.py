from django.contrib.auth import get_user_model
from customers.models import CustomerModel

User = get_user_model()

def GetOrCreateUserByPhoneService(phone_number: str):
    """دریافت یا ساخت کاربر و پروفایل مشتری"""
    user, created = User.objects.get_or_create(
        phone_number=phone_number,
        defaults={
            'username': phone_number,
            'role': 'CUSTOMER'
        }
    )
    if created:
        CustomerModel.objects.create(user=user)
    return user, created