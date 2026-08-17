from salon_services import models


def DeleteServiceService(service_id: int) -> bool:
    """
    حذف یک خدمت از سالن
    """
    try:
        service = models.ServiceModel.objects.get(id=service_id)
        service.delete()
        return True
    except models.ServiceModel.DoesNotExist:
        return False