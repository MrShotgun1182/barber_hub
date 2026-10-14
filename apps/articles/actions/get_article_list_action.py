from articles import services as articles_services
from tags import services as tags_services


def GetPublicArticlesListAction(
    search: str = None,
    tag_slug: str = None,
    author_id: int = None,
    sort: str = 'newest',
) -> dict:
    """اکشن دریافت داده صفحه عمومی مقالات (ویژه‌ها، لیست، برچسب‌ها، نویسندگان)"""
    try:
        articles = list(
            articles_services.GetPublishedArticlesService(
                search=search, tag_slug=tag_slug, author_id=author_id, sort=sort
            )
        )
        featured = list(articles_services.GetFeaturedArticlesService())
        tags = list(tags_services.GetAllTagsService())
        authors = articles_services.GetPublishedAuthorsService()
        return {
            'status': 'success',
            'message': '',
            'articles': articles,
            'featured': featured,
            'tags': tags,
            'authors': authors,
        }
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت مقالات.'}


def GetArticleDetailAction(slug: str) -> dict:
    """اکشن دریافت جزئیات مقاله منتشرشده و افزایش شمارنده بازدید"""
    try:
        article = articles_services.GetArticleBySlugService(slug=slug)
        articles_services.IncrementArticleViewsService(article_id=article.id)
        return {'status': 'success', 'message': '', 'article': article}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت مقاله.'}


def GetBarberArticlesAction(author) -> dict:
    """اکشن دریافت مقالات نویسنده برای پنل آرایشگر"""
    try:
        articles = list(articles_services.GetArticlesByAuthorService(author=author))
        return {'status': 'success', 'message': '', 'articles': articles}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت مقالات شما.'}


def GetModerationQueueAction(status: str = None, search: str = None) -> dict:
    """اکشن دریافت صف بازبینی مقالات برای پنل مدیر"""
    try:
        articles = list(
            articles_services.GetArticlesForModerationService(
                status=status, search=search
            )
        )
        return {'status': 'success', 'message': '', 'articles': articles}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت صف بازبینی.'}
