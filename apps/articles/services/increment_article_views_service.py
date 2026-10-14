from django.db.models import F
from articles import models as articles_models


def IncrementArticleViewsService(article_id: int) -> None:
    """افزایش شمارنده بازدید مقاله به‌صورت اتمیک (ایمن در برابر هم‌زمانی)"""
    articles_models.ArticleModel.objects.filter(id=article_id).update(
        views_count=F('views_count') + 1
    )
