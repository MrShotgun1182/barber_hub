from store import services as store_services


def GetProductDetailAction(product_id: int) -> dict:
    """اکشن دریافت داده صفحه جزئیات محصول"""
    try:
        product = store_services.GetProductDetailService(product_id)
        return {
            'status': 'success',
            'message': '',
            'product': product,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت اطلاعات محصول.'}
