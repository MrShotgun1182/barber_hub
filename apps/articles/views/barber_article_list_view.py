from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from articles import actions


@login_required
def BarberArticleListView(request):
    """ویوی لیست مقالات خودِ آرایشگر (با نمایش وضعیت و دلیل رد)"""
    barber = getattr(request.user, 'barber_profile', None)
    if not barber:
        return redirect('barbers:barbers_login')

    data = actions.GetBarberArticlesAction(request.user)
    context = {
        'articles': data.get('articles', []),
        'error_message': data.get('message') if data['status'] == 'error' else None,
    }
    return render(request, 'articles/barber/article_list.html', context)
