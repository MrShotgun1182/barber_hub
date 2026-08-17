from typing import Optional
from django.core.files.uploadedfile import UploadedFile
from customers import models


def CreateCustomerHairstyleService(
    customer: models.CustomerModel,
    image: UploadedFile,
    title: Optional[str] = None,
    notes: Optional[str] = None,
) -> models.CustomerHairstyleModel:
    """
    ایجاد و ذخیره تصویر مدل موی جدید برای مشتری
    """
    return models.CustomerHairstyleModel.objects.create(
        customer=customer,
        image=image,
        title=title,
        notes=notes,
    )