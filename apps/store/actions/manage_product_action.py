from store import services as store_services


def CreateProductAction(
    title: str,
    price: int,
    category_id: int,
    description: str = '',
    is_published: bool = False,
    is_orderable: bool = True,
    image_files: list = None,
) -> dict:
    """اکشن ایجاد محصول جدید با تصاویر"""
    try:
        product = store_services.CreateProductService(
            title=title,
            price=price,
            category_id=category_id,
            description=description,
            is_published=is_published,
            is_orderable=is_orderable,
            image_files=image_files,
        )
        return {
            'status': 'success',
            'message': 'محصول با موفقیت ایجاد شد.',
            'product': product,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در ایجاد محصول.'}


def UpdateProductAction(product_id: int, image_files: list = None, **fields) -> dict:
    """اکشن به‌روزرسانی محصول و افزودن تصاویر جدید"""
    try:
        product = store_services.UpdateProductService(
            product_id, image_files=image_files, **fields
        )
        return {
            'status': 'success',
            'message': 'محصول با موفقیت به‌روزرسانی شد.',
            'product': product,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در به‌روزرسانی محصول.'}


def DeleteProductAction(product_id: int) -> dict:
    """اکشن حذف نرم محصول"""
    try:
        store_services.DeleteProductService(product_id)
        return {'status': 'success', 'message': 'محصول با موفقیت حذف شد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در حذف محصول.'}


def ToggleProductFieldAction(product_id: int, field: str) -> dict:
    """اکشن تغییر وضعیت انتشار یا سفارش‌پذیری محصول"""
    try:
        store_services.ToggleProductFieldService(product_id, field)
        return {'status': 'success', 'message': 'وضعیت محصول تغییر کرد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در تغییر وضعیت محصول.'}
