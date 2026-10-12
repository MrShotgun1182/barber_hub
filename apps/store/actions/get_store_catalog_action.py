from store import services as store_services


def GetStoreCatalogAction(category_id: int = None, search: str = None) -> dict:
    """اکشن دریافت داده صفحه اصلی فروشگاه (دسته‌بندی‌ها و محصولات)"""
    try:
        categories = list(store_services.GetActiveCategoriesService())
        products = list(
            store_services.GetPublishedProductsService(
                category_id=category_id, search=search
            )
        )
        return {
            'status': 'success',
            'message': '',
            'categories': categories,
            'products': products,
        }
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت محصولات فروشگاه.'}
