from tags import services as tags_services


def GetAllTagsAction() -> dict:
    """اکشن دریافت همه برچسب‌ها"""
    try:
        tags = list(tags_services.GetAllTagsService())
        return {'status': 'success', 'message': '', 'tags': tags}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت برچسب‌ها.'}


def CreateTagAction(name: str) -> dict:
    """اکشن ایجاد برچسب جدید"""
    try:
        tag = tags_services.CreateTagService(name=name)
        return {
            'status': 'success',
            'message': 'برچسب با موفقیت ایجاد شد.',
            'tag': tag,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در ایجاد برچسب.'}


def UpdateTagAction(tag_id: int, name: str) -> dict:
    """اکشن به‌روزرسانی برچسب"""
    try:
        tag = tags_services.UpdateTagService(tag_id=tag_id, name=name)
        return {
            'status': 'success',
            'message': 'برچسب با موفقیت به‌روزرسانی شد.',
            'tag': tag,
        }
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در به‌روزرسانی برچسب.'}


def DeleteTagAction(tag_id: int) -> dict:
    """اکشن حذف برچسب"""
    try:
        tags_services.DeleteTagService(tag_id=tag_id)
        return {'status': 'success', 'message': 'برچسب با موفقیت حذف شد.'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در حذف برچسب.'}


def GetTagByIdAction(tag_id: int) -> dict:
    """اکشن دریافت یک برچسب برای فرم ویرایش"""
    try:
        tag = tags_services.GetTagByIdService(tag_id=tag_id)
        return {'status': 'success', 'message': '', 'tag': tag}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'خطا در دریافت برچسب.'}
