from django.test import TestCase

from tags import models as tags_models
from tags import services as tags_services


class TagServiceTests(TestCase):
    """تست‌های سرویس‌های برچسب: ساخت، اسلاگ، به‌روزرسانی و حذف"""

    def test_create_tag_generates_slug(self):
        tag = tags_services.CreateTagService('اصلاح مو')
        self.assertEqual(tag.name, 'اصلاح مو')
        self.assertEqual(tag.slug, 'اصلاح-مو')
        self.assertTrue(tag.id)

    def test_create_tag_empty_name_fails(self):
        with self.assertRaises(ValueError):
            tags_services.CreateTagService('   ')

    def test_create_duplicate_name_fails(self):
        tags_services.CreateTagService('اصلاح مو')
        with self.assertRaises(ValueError):
            tags_services.CreateTagService('اصلاح مو')

    def test_duplicate_name_gets_numeric_suffix(self):
        first = tags_services.CreateTagService('اصلاح مو')
        second = tags_services.CreateTagService('اصلاح  مو')
        # نام متفاوت است ولی اسلاگ یکسان تولید می‌شود؛ پسوند عددی یکتایی را تضمین می‌کند
        self.assertNotEqual(first.slug, second.slug)
        self.assertTrue(second.slug.startswith('اصلاح-مو-'))

    def test_update_tag_regenerates_slug(self):
        tag = tags_services.CreateTagService('اصلاح مو')
        updated = tags_services.UpdateTagService(tag.id, 'رنگ مو')
        self.assertEqual(updated.name, 'رنگ مو')
        self.assertEqual(updated.slug, 'رنگ-مو')

    def test_update_tag_to_duplicate_name_fails(self):
        tags_services.CreateTagService('اصلاح مو')
        other = tags_services.CreateTagService('رنگ مو')
        with self.assertRaises(ValueError):
            tags_services.UpdateTagService(other.id, 'اصلاح مو')

    def test_update_missing_tag_fails(self):
        with self.assertRaises(ValueError):
            tags_services.UpdateTagService(999, 'رنگ مو')

    def test_delete_tag_removes_it(self):
        tag = tags_services.CreateTagService('اصلاح مو')
        tags_services.DeleteTagService(tag.id)
        self.assertFalse(tags_models.TagModel.objects.filter(id=tag.id).exists())
