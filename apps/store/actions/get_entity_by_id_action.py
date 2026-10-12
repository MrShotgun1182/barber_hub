from store import services as store_services


def GetCategoryByIdAction(category_id: int) -> dict:
    """اکشن دریافت یک دسته‌بندی برای فرم ویرایش مدیر"""
    category = store_services.GetCategoryByIdService(category_id)
    if category is None:
        return {'status': 'error', 'message': 'دسته‌بندی مورد نظر یافت نشد.'}
    return {'status': 'success', 'message': '', 'category': category}


def GetProductByIdAction(product_id: int) -> dict:
    """اکشن دریافت یک محصول برای فرم ویرایش مدیر"""
    product = store_services.GetProductByIdService(product_id)
    if product is None:
        return {'status': 'error', 'message': 'محصول مورد نظر یافت نشد.'}
    return {'status': 'success', 'message': '', 'product': product}


def GetOrderByIdAction(order_id: int) -> dict:
    """اکشن دریافت یک سفارش برای صفحه جزئیات مدیر"""
    order = store_services.GetOrderByIdService(order_id)
    if order is None:
        return {'status': 'error', 'message': 'سفارش مورد نظر یافت نشد.'}
    return {'status': 'success', 'message': '', 'order': order}
