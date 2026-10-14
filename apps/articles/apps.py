from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    """کانفیگ اپ مقالات"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
    verbose_name = 'مقالات'
