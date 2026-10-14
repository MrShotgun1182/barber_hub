from django.contrib import admin
from tags import models as tags_models


@admin.register(tags_models.TagModel)
class TagAdmin(admin.ModelAdmin):
    """ادمین جنگو برای برچسب‌ها"""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
