from django.contrib import messages
from django.shortcuts import redirect, render
from store import actions


def _IsManager(request) -> bool:
    """بررسی دسترسی مدیر فروشگاه"""
    return request.user.is_authenticated and (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    )


def ManageCategoryListView(request):
    """ویوی لیست دسته‌بندی‌های محصول در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    data = actions.GetManageCatalogAction()
    context = {
        'categories': data.get('categories', []),
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'store/manager/category_list.html', context)


def ManageCategoryFormView(request, category_id: int = None):
    """ویوی فرم ایجاد/ویرایش دسته‌بندی محصول در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    category = None
    if category_id:
        data = actions.GetCategoryByIdAction(category_id)
        category = data.get('category')

    # مقادیر اولیه فرم: ویرایش → مقادیر ذخیره‌شده؛ در غیر این صورت خالی
    form_name = category.name if category else ''
    form_description = category.description if category else ''

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            context = {
                'category': category,
                'error_message': 'نام دسته‌بندی الزامی است.',
                'form_name': name,
                'form_description': description,
            }
            return render(request, 'store/manager/category_form.html', context)

        if category:
            data = actions.UpdateCategoryAction(
                category.id, name=name, description=description
            )
        else:
            data = actions.CreateCategoryAction(name, description=description)

        if data['status'] == 'success':
            return redirect('store:manage_category_list')
        context = {
            'category': category,
            'error_message': data['message'],
            'form_name': name,
            'form_description': description,
        }
        return render(request, 'store/manager/category_form.html', context)

    context = {'category': category, 'form_name': form_name, 'form_description': form_description}
    return render(request, 'store/manager/category_form.html', context)


def ManageCategoryDeleteView(request, category_id: int):
    """ویوی حذف دسته‌بندی محصول در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    if request.method == 'POST':
        data = actions.DeleteCategoryAction(category_id)
        if data['status'] == 'error':
            messages.error(request, data['message'])
    return redirect('store:manage_category_list')
