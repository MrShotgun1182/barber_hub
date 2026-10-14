from django.contrib import admin
from articles import models as articles_models


class ArticleImageInline(admin.TabularInline):
    """نمایش تصاویر گالری مقاله به‌صورت درون‌خطی"""

    model = articles_models.ArticleImageModel
    extra = 0


@admin.register(articles_models.ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    """ادمین جنگو برای مقالات"""

    list_display = (
        'title',
        'author',
        'status',
        'is_featured',
        'views_count',
        'published_at',
        'created_at',
    )
    list_filter = ('status', 'is_featured')
    search_fields = ('title', 'author__username', 'author__phone_number')
    inlines = (ArticleImageInline,)
