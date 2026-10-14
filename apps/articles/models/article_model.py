from django.conf import settings
from django.db import models
from tags import models as tags_models


class ArticleModel(models.Model):
    """مقاله با چرخه بازبینی: آرایشگر ذخیره می‌کند و مدیر منتشر/رد/بایگانی می‌کند"""

    STATUS_CHOICES = (
        ('DRAFT', 'پیش‌نویس'),
        ('PENDING', 'در انتظار تایید'),
        ('PUBLISHED', 'منتشر شده'),
        ('REJECTED', 'رد شده'),
        ('ARCHIVED', 'بایگانی شده'),
    )

    title = models.CharField(max_length=255, verbose_name='عنوان مقاله')
    slug = models.SlugField(
        max_length=255, unique=True, allow_unicode=True, verbose_name='اسلاگ'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='نویسنده',
    )
    cover_image = models.ImageField(
        upload_to='articles/covers/', verbose_name='تصویر شاخص'
    )
    content = models.TextField(verbose_name='محتوای مقاله')
    tags = models.ManyToManyField(
        tags_models.TagModel,
        blank=True,
        related_name='articles',
        verbose_name='برچسب‌ها',
    )
    is_featured = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='وضعیت',
        db_index=True,
    )
    rejection_reason = models.TextField(
        blank=True, null=True, verbose_name='دلیل رد مقاله'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    published_at = models.DateTimeField(
        blank=True, null=True, verbose_name='تاریخ انتشار'
    )

    # وضعیت «پیش‌نویس» برای توسعه آینده نگه داشته شده؛ جریان فعلی هیچ‌گاه آن را تنظیم نمی‌کند

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-created_at']

    def __str__(self):
        return f'مقاله: {self.title}'
