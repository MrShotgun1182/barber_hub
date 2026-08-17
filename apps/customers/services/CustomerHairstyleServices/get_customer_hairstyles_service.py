from django.db.models import QuerySet
from customers import models


def GetCustomerHairstylesService(
    customer: models.CustomerModel,
) -> QuerySet[models.CustomerHairstyleModel]:
    """
    دریافت لیست تمام مدل‌های موی ثبت‌شده برای یک مشتری
    """
    return models.CustomerHairstyleModel.objects.filter(customer=customer)