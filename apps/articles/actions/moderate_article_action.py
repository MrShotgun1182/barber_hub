from articles import services as articles_services


def PublishArticleAction(article_id: int) -> dict:
    """اکشن انتشار مقاله در صف بازبینی"""
    try:
        article = articles_services.PublishArticleService(article_id=article_id)
        return {
            'status': 'success',
            'message': 'مقاله با موفقیت منتشر شد.',
            'article': article,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در انتشار مقاله.'}


def RejectArticleAction(article_id: int, reason: str) -> dict:
    """اکشن رد مقاله همراه با دلیل برای نویسنده"""
    try:
        article = articles_services.RejectArticleService(
            article_id=article_id, reason=reason
        )
        return {
            'status': 'success',
            'message': 'مقاله رد شد و دلیل آن برای نویسنده ثبت شد.',
            'article': article,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در رد مقاله.'}


def ArchiveArticleAction(article_id: int) -> dict:
    """اکشن بایگانی مقاله منتشرشده"""
    try:
        article = articles_services.ArchiveArticleService(article_id=article_id)
        return {
            'status': 'success',
            'message': 'مقاله بایگانی شد.',
            'article': article,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در بایگانی مقاله.'}


def ToggleArticleFeaturedAction(article_id: int) -> dict:
    """اکشن تغییر وضعیت ویژه بودن مقاله"""
    try:
        article = articles_services.ToggleArticleFeaturedService(article_id=article_id)
        return {
            'status': 'success',
            'message': 'وضعیت ویژه مقاله تغییر کرد.',
            'article': article,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در تغییر وضعیت ویژه مقاله.'}
