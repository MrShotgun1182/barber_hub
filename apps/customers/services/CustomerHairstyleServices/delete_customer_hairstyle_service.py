from customers import models


def DeleteCustomerHairstyleService(hairstyle_id: int) -> bool:
    """
    حذف یک مدل موی ثبت‌شده برای مشتری
    """
    try:
        hairstyle = models.CustomerHairstyleModel.objects.get(id=hairstyle_id)
        hairstyle.delete()
        return True
    except models.CustomerHairstyleModel.DoesNotExist:
        return False