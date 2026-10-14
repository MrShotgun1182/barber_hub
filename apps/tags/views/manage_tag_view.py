from django.contrib import messages
from django.shortcuts import redirect, render
from tags import actions


def _IsManager(request) -> bool:
    """بررسی دسترسی مدیر (برچسب‌ها فقط توسط مدیر مدیریت می‌شوند)"""
    return request.user.is_authenticated and (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    )


def ManageTagListView(request):
    """ویوی لیست برچسب‌ها در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    data = actions.GetAllTagsAction()
    context = {
        'tags': data.get('tags', []),
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'tags/manager/tag_list.html', context)


def ManageTagFormView(request, tag_id: int = None):
    """ویوی فرم ایجاد/ویرایش برچسب در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    tag = None
    if tag_id:
        tag = actions.GetTagByIdAction(tag_id).get('tag')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if not name:
            context = {
                'tag': tag,
                'error_message': 'نام برچسب الزامی است.',
                'form_name': name,
            }
            return render(request, 'tags/manager/tag_form.html', context)

        if tag:
            data = actions.UpdateTagAction(tag.id, name=name)
        else:
            data = actions.CreateTagAction(name)

        if data['status'] == 'success':
            return redirect('tags:manage_tag_list')
        context = {
            'tag': tag,
            'error_message': data['message'],
            'form_name': name,
        }
        return render(request, 'tags/manager/tag_form.html', context)

    context = {'tag': tag, 'form_name': tag.name if tag else ''}
    return render(request, 'tags/manager/tag_form.html', context)


def ManageTagDeleteView(request, tag_id: int):
    """ویوی حذف برچسب در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    if request.method == 'POST':
        data = actions.DeleteTagAction(tag_id)
        if data['status'] == 'error':
            messages.error(request, data['message'])
    return redirect('tags:manage_tag_list')
