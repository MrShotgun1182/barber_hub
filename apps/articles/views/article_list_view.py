from django.shortcuts import render
from articles import actions


def ArticleListView(request):
    """ویوی صفحه عمومی لیست مقالات منتشرشده (جستجو، فیلتر و مرتب‌سازی)"""
    search = request.GET.get('search', '').strip()
    tag_slug = request.GET.get('tag', '').strip() or None
    sort = request.GET.get('sort', 'newest')

    # فیلتر نویسنده فقط اگر عدد معتبر ارسال شده باشد اعمال می‌شود
    author_id = request.GET.get('author')
    if author_id and author_id.isdigit():
        author_id = int(author_id)
    else:
        author_id = None

    # ۱. مقاله‌های ویژه هنگام جستجو/فیلتر نمایش داده نمی‌شوند تا صفحه شلوغ نشود
    if search or tag_slug or author_id:
        featured = []
    else:
        featured = None

    data = actions.GetPublicArticlesListAction(
        search=search, tag_slug=tag_slug, author_id=author_id, sort=sort
    )

    context = {
        'articles': data.get('articles', []),
        'featured': featured if featured is not None else data.get('featured', []),
        'tags': data.get('tags', []),
        'authors': data.get('authors', []),
        'search': search,
        'selected_tag_slug': tag_slug,
        'selected_author_id': author_id,
        'sort': sort if sort in ('newest', 'views') else 'newest',
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'articles/article_list.html', context)
