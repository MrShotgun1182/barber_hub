from articles import services as articles_services


def CreateArticleAction(
    author,
    title: str,
    content: str,
    cover_image,
    tag_ids: list = None,
    gallery_files: list = None,
    publish: bool = False,
    is_featured: bool = False,
) -> dict:
    """اکشن ایجاد مقاله جدید با تصاویر و برچسب‌ها"""
    try:
        article = articles_services.CreateArticleService(
            author=author,
            title=title,
            content=content,
            cover_image=cover_image,
            tag_ids=tag_ids,
            gallery_files=gallery_files,
            publish=publish,
            is_featured=is_featured,
        )
        return {
            'status': 'success',
            'message': 'مقاله با موفقیت ایجاد شد.',
            'article': article,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در ایجاد مقاله.'}


def UpdateArticleAction(
    article_id: int,
    editor,
    title: str,
    content: str,
    cover_image=None,
    tag_ids: list = None,
    gallery_files: list = None,
    publish: bool = False,
) -> dict:
    """اکشن به‌روزرسانی مقاله (بازگشت به صف بازبینی در صورت ویرایش آرایشگر)"""
    try:
        article = articles_services.UpdateArticleService(
            article_id=article_id,
            editor=editor,
            title=title,
            content=content,
            cover_image=cover_image,
            tag_ids=tag_ids,
            gallery_files=gallery_files,
            publish=publish,
        )
        return {
            'status': 'success',
            'message': 'مقاله با موفقیت به‌روزرسانی شد.',
            'article': article,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در به‌روزرسانی مقاله.'}


def DeleteArticleAction(article_id: int, requester) -> dict:
    """اکشن حذف دائمی مقاله"""
    try:
        articles_services.DeleteArticleService(article_id=article_id, requester=requester)
        return {'status': 'success', 'message': 'مقاله با موفقیت حذف شد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در حذف مقاله.'}


def GetArticleByIdAction(article_id: int) -> dict:
    """اکشن دریافت مقاله برای فرم ویرایش"""
    try:
        article = articles_services.GetArticleByIdService(article_id=article_id)
        return {'status': 'success', 'message': '', 'article': article}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت مقاله.'}
