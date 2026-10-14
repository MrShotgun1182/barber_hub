from django.db import models
from articles.models import ArticleModel


class ArticleImageModel(models.Model):
    """تصویر گالری الحاقی مقاله (تصویر شاخص فیلد جداگانه مدل مقاله است)"""

    article = models.ForeignKey(
        ArticleModel,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='مقاله',
    )
    image = models.ImageField(upload_to='articles/gallery/', verbose_name='تصویر')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'تصویر مقاله'
        verbose_name_plural = 'تصاویر مقالات'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'تصویر {self.article.title}'
