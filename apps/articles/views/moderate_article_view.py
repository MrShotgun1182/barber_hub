from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from articles import actions
from articles.views.manage_article_list_view import _IsManager


@require_POST
def ModerateArticleView(request, article_id: int):
    """ویوی عملیات بازبینی مقاله (انتشار/رد/بایگانی) توسط مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    action_type = request.POST.get('action', '')

    if action_type == 'publish':
        data = actions.PublishArticleAction(article_id)
    elif action_type == 'reject':
        reason = request.POST.get('reason', '').strip()
        data = actions.RejectArticleAction(article_id, reason=reason)
    elif action_type == 'archive':
        data = actions.ArchiveArticleAction(article_id)
    else:
        data = {'status': 'error', 'message': 'عملیات بازبینی نامعتبر است.'}

    if data['status'] == 'error':
        messages.error(request, data['message'])
    else:
        messages.success(request, data['message'])
    return redirect('articles_manager:manage_article_list')


@require_POST
def ManageArticleFeaturedToggleView(request, article_id: int):
    """ویوی تغییر وضعیت ویژه بودن مقاله در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    data = actions.ToggleArticleFeaturedAction(article_id)
    if data['status'] == 'error':
        messages.error(request, data['message'])
    return redirect('articles_manager:manage_article_list')
