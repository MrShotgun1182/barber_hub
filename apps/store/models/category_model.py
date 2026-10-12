from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name='نام دسته‌بندی'
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='توضیحات'
    )
    is_active = models.BooleanField(default=True, verbose_name='وضعیت فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'دسته‌بندی محصول'
        verbose_name_plural = 'دسته‌بندی محصولات'
        ordering = ['name']

    def __str__(self):
        return self.name
