from django.db import transaction
from articles import models as articles_models


def _IsManagerUser(user) -> bool:
    """بررسی نقش مدیر برای مالکیت حذف/ویرایش مقاله دیگران"""
    return getattr(user, 'role', None) == 'MANAGER' or user.is_staff or user.is_superuser


def DeleteArticleService(article_id: int, requester) -> None:
    """حذف دائمی مقاله (فقط نویسنده یا مدیر)"""
    with transaction.atomic():
        try:
            article = articles_models.ArticleModel.objects.get(id=article_id)
        except articles_models.ArticleModel.DoesNotExist:
            raise ValueError('مقاله مورد نظر یافت نشد.')

        if article.author_id != requester.id and not _IsManagerUser(requester):
            raise ValueError('اجازه حذف این مقاله را ندارید.')

        article.delete()
