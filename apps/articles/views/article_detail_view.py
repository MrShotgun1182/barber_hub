from django.shortcuts import render
from articles import actions


def ArticleDetailView(request, slug: str):
    """ویوی صفحه جزئیات مقاله منتشرشده (با افزایش شمارنده بازدید)"""
    data = actions.GetArticleDetailAction(slug=slug)

    if data['status'] == 'error':
        context = {'error_message': data['message']}
        return render(request, 'articles/article_not_found.html', context, status=404)

    context = {'article': data['article']}
    return render(request, 'articles/article_detail.html', context)
