from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from articles import actions
from tags import services as tags_services


@login_required
def BarberArticleFormView(request, article_id: int = None):
    """ویوی فرم ایجاد/ویرایش مقاله توسط آرایشگر (ذخیره → در انتظار تایید)"""
    barber = getattr(request.user, 'barber_profile', None)
    if not barber:
        return redirect('barbers:barbers_login')

    # ۱. دریافت مقاله در حالت ویرایش
    article = None
    if article_id:
        article = actions.GetArticleByIdAction(article_id).get('article')
        if not article or article.author_id != request.user.id:
            context = {
                'tags': list(tags_services.GetAllTagsService()),
                'error_message': 'اجازه ویرایش این مقاله را ندارید.',
            }
            return render(request, 'articles/barber/article_form.html', context, status=403)

    # ۲. مقادیر اولیه فرم برای رندر مجدد پس از خطا
    form_values = {
        'title': article.title if article else '',
        'content': article.content if article else '',
        'selected_tag_ids': [tag.id for tag in article.tags.all()] if article else [],
    }

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        cover_image = request.FILES.get('cover_image')
        gallery_files = request.FILES.getlist('gallery')
        tag_ids = [int(tag_id) for tag_id in request.POST.getlist('tags') if tag_id.isdigit()]

        # ۳. تصویر شاخص در ایجاد الزامی است؛ در ویرایش فقط اگر ارسال شود جایگزین می‌شود
        if article:
            data = actions.UpdateArticleAction(
                article_id=article.id,
                editor=request.user,
                title=title,
                content=content,
                cover_image=cover_image,
                tag_ids=tag_ids,
                gallery_files=gallery_files,
            )
        else:
            data = actions.CreateArticleAction(
                author=request.user,
                title=title,
                content=content,
                cover_image=cover_image,
                tag_ids=tag_ids,
                gallery_files=gallery_files,
            )

        # ۴. در صورت موفقیت به لیست مقالات برمی‌گردیم؛ در غیر این صورت فرم با خطا رندر می‌شود
        if data['status'] == 'success':
            return redirect('articles_barber:barber_article_list')

        form_values.update({'title': title, 'content': content, 'selected_tag_ids': tag_ids})
        context = {
            'article': article,
            'tags': list(tags_services.GetAllTagsService()),
            'error_message': data['message'],
            **form_values,
        }
        return render(request, 'articles/barber/article_form.html', context)

    context = {
        'article': article,
        'tags': list(tags_services.GetAllTagsService()),
        **form_values,
    }
    return render(request, 'articles/barber/article_form.html', context)
