from django.db import models
from store import models as store_models


class ProductModel(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان محصول')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات و مشخصات')
    price = models.PositiveIntegerField(verbose_name='قیمت (تومان)')
    category = models.ForeignKey(
        store_models.CategoryModel,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='دسته‌بندی',
    )
    is_published = models.BooleanField(default=False, verbose_name='وضعیت انتشار')
    is_orderable = models.BooleanField(default=True, verbose_name='قابل سفارش')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف‌شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        """تصویر اصلی محصول (اولین تصویر با is_main=True؛ در صورت نبود، اولین تصویر)"""
        images = getattr(self, 'images', None)
        if images is None:
            return None
        all_images = list(images.all())
        if not all_images:
            return None
        for image in all_images:
            if image.is_main:
                return image
        return all_images[0]
