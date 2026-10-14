from django.contrib import messages
from django.shortcuts import redirect, render
from articles import actions


def _IsManager(request) -> bool:
    """بررسی دسترسی مدیر (بازبینی مقالات فقط توسط مدیر انجام می‌شود)"""
    return request.user.is_authenticated and (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    )


def ManageArticleListView(request):
    """ویوی صف بازبینی مقالات در پنل مدیر (تب وضعیت و جستجو)"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    status = request.GET.get('status', '').strip()
    search = request.GET.get('search', '').strip()

    data = actions.GetModerationQueueAction(status=status or None, search=search or None)
    context = {
        'articles': data.get('articles', []),
        'current_status': status if status in ('PENDING', 'PUBLISHED', 'REJECTED', 'ARCHIVED') else '',
        'search': search,
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'articles/manager/article_list.html', context)


def ManageArticleFormView(request, article_id: int = None):
    """ویوی فرم ایجاد/ویرایش مقاله توسط مدیر (با انتشار فوری و ویژه)"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    # ۱. دریافت مقاله در حالت ویرایش
    article = None
    if article_id:
        article = actions.GetArticleByIdAction(article_id).get('article')

    from tags import services as tags_services
    tags = list(tags_services.GetAllTagsService())

    form_values = {
        'title': article.title if article else '',
        'content': article.content if article else '',
        'is_featured': article.is_featured if article else False,
        'selected_tag_ids': [tag.id for tag in article.tags.all()] if article else [],
    }

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        cover_image = request.FILES.get('cover_image')
        gallery_files = request.FILES.getlist('gallery')
        tag_ids = [int(tag_id) for tag_id in request.POST.getlist('tags') if tag_id.isdigit()]
        publish_now = request.POST.get('publish_now') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'

        # ۲. فراخوانی اکشن متناسب (ایجاد یا به‌روزرسانی)
        if article:
            data = actions.UpdateArticleAction(
                article_id=article.id,
                editor=request.user,
                title=title,
                content=content,
                cover_image=cover_image,
                tag_ids=tag_ids,
                gallery_files=gallery_files,
                publish=publish_now,
            )
        else:
            data = actions.CreateArticleAction(
                author=request.user,
                title=title,
                content=content,
                cover_image=cover_image,
                tag_ids=tag_ids,
                gallery_files=gallery_files,
                publish=publish_now,
                is_featured=is_featured,
            )

        # ۳. در صورت موفقیت به صف بازبینی برمی‌گردیم
        if data['status'] == 'success':
            return redirect('articles_manager:manage_article_list')

        form_values.update(
            {
                'title': title,
                'content': content,
                'is_featured': is_featured,
                'selected_tag_ids': tag_ids,
            }
        )
        context = {
            'article': article,
            'tags': tags,
            'error_message': data['message'],
            **form_values,
        }
        return render(request, 'articles/manager/article_form.html', context)

    context = {'article': article, 'tags': tags, **form_values}
    return render(request, 'articles/manager/article_form.html', context)


def ManageArticleDeleteView(request, article_id: int):
    """ویوی حذف دائمی مقاله در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    if request.method == 'POST':
        data = actions.DeleteArticleAction(article_id, requester=request.user)
        if data['status'] == 'error':
            messages.error(request, data['message'])
    return redirect('articles_manager:manage_article_list')
