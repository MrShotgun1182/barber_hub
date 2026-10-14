from django.apps import AppConfig


class TagsConfig(AppConfig):
    """کانفیگ اپ برچسب‌های مقالات"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'
    verbose_name = 'برچسب‌ها'
