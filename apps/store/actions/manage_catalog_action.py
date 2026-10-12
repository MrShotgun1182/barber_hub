from store import services as store_services


def GetManageCatalogAction() -> dict:
    """اکشن دریافت داده پنل مدیریت دسته‌بندی‌ها و محصولات"""
    try:
        categories = list(store_services.GetAllCategoriesService())
        products = list(store_services.GetAllProductsService())
        return {
            'status': 'success',
            'message': '',
            'categories': categories,
            'products': products,
        }
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت داده‌های مدیریت فروشگاه.'}


def CreateCategoryAction(name: str, description: str = '') -> dict:
    """اکشن ایجاد دسته‌بندی جدید محصول"""
    try:
        category = store_services.CreateCategoryService(
            name=name, description=description
        )
        return {
            'status': 'success',
            'message': 'دسته‌بندی با موفقیت ایجاد شد.',
            'category': category,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در ایجاد دسته‌بندی.'}


def UpdateCategoryAction(category_id: int, **fields) -> dict:
    """اکشن به‌روزرسانی دسته‌بندی محصول"""
    try:
        category = store_services.UpdateCategoryService(category_id, **fields)
        return {
            'status': 'success',
            'message': 'دسته‌بندی با موفقیت به‌روزرسانی شد.',
            'category': category,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در به‌روزرسانی دسته‌بندی.'}


def DeleteCategoryAction(category_id: int) -> dict:
    """اکشن حذف دسته‌بندی محصول"""
    try:
        store_services.DeleteCategoryService(category_id)
        return {'status': 'success', 'message': 'دسته‌بندی با موفقیت حذف شد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در حذف دسته‌بندی.'}
