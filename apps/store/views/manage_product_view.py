from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from store import actions


def _IsManager(request) -> bool:
    """بررسی دسترسی مدیر فروشگاه"""
    return request.user.is_authenticated and (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    )


def _ProductFormContext(product) -> dict:
    """داده کمکی فرم محصول: لیست دسته‌بندی‌ها"""
    from store import services as store_services

    categories = list(store_services.GetAllCategoriesService())
    return {'product': product, 'categories': categories}


def ManageProductListView(request):
    """ویوی لیست محصولات در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    data = actions.GetManageCatalogAction()
    context = {
        'products': data.get('products', []),
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'store/manager/product_list.html', context)


def ManageProductFormView(request, product_id: int = None):
    """ویوی فرم ایجاد/ویرایش محصول (با آپلود تصاویر) در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    product = None
    if product_id:
        product = actions.GetProductByIdAction(product_id).get('product')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price_raw = request.POST.get('price', '').strip()
        category_id_raw = request.POST.get('category', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        is_orderable = request.POST.get('is_orderable') == 'on'
        image_files = request.FILES.getlist('images')

        # ۱. اعتبارسنجی ورودی‌های عددی
        try:
            price = int(price_raw)
            category_id = int(category_id_raw)
        except (TypeError, ValueError):
            context = _ProductFormContext(product)
            context['error_message'] = 'قیمت و دسته‌بندی باید عدد باشند.'
            return render(request, 'store/manager/product_form.html', context)

        fields = {
            'title': title,
            'description': description,
            'price': price,
            'category_id': category_id,
            'is_published': is_published,
            'is_orderable': is_orderable,
        }

        # ۲. فراخوانی اکشن متناسب (ایجاد یا به‌روزرسانی)
        if product:
            data = actions.UpdateProductAction(
                product.id, image_files=image_files, **fields
            )
        else:
            data = actions.CreateProductAction(image_files=image_files, **fields)

        if data['status'] == 'success':
            return redirect('store:manage_product_list')

        context = _ProductFormContext(product)
        context['error_message'] = data['message']
        return render(request, 'store/manager/product_form.html', context)

    context = _ProductFormContext(product)
    return render(request, 'store/manager/product_form.html', context)


def ManageProductDeleteView(request, product_id: int):
    """ویوی حذف نرم محصول در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    if request.method == 'POST':
        data = actions.DeleteProductAction(product_id)
        if data['status'] == 'error':
            messages.error(request, data['message'])
    return redirect('store:manage_product_list')


@require_POST
def ManageProductToggleView(request, product_id: int):
    """ویوی تغییر وضعیت انتشار یا سفارش‌پذیری محصول در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    field = request.POST.get('field', '')
    data = actions.ToggleProductFieldAction(product_id, field)
    if data['status'] == 'error':
        messages.error(request, data['message'])
    return redirect('store:manage_product_list')
