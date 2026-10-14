from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from articles import actions


@login_required
def BarberArticleDeleteView(request, article_id: int):
    """ویوی حذف مقاله خودِ آرایشگر"""
    barber = getattr(request.user, 'barber_profile', None)
    if not barber:
        return redirect('barbers:barbers_login')

    if request.method == 'POST':
        data = actions.DeleteArticleAction(article_id, requester=request.user)
        if data['status'] == 'error':
            messages.error(request, data['message'])
    return redirect('articles_barber:barber_article_list')
