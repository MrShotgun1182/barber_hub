from tags import models as tags_models


def GetAllTagsService():
    """دریافت همه برچسب‌ها برای لیست مدیر و سلکتور مقالات"""
    return tags_models.TagModel.objects.all()


def GetTagByIdService(tag_id: int) -> tags_models.TagModel:
    """دریافت یک برچسب بر اساس شناسه"""
    try:
        return tags_models.TagModel.objects.get(id=tag_id)
    except tags_models.TagModel.DoesNotExist:
        raise ValueError('برچسب مورد نظر یافت نشد.')
