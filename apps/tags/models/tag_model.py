from django.db import models


class TagModel(models.Model):
    """برچسب دسته‌بندی مقالات (فقط مدیر می‌تواند بسازد)"""

    name = models.CharField(max_length=50, unique=True, verbose_name='نام برچسب')
    slug = models.SlugField(
        max_length=100, unique=True, allow_unicode=True, verbose_name='اسلاگ'
    )

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name
