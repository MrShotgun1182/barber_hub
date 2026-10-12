from store import models as store_models
from store import services as store_services

from .test_cart_services import BaseStoreTestCase


class RevalidationTests(BaseStoreTestCase):
    """تست‌های بازبینی سبد پیش از ثبت سفارش: تغییر قیمت و غیرقابل‌سفارش شدن"""

    def _seed_cart(self):
        store_services.AddToCartService(self.customer, self.product.id, quantity=2)

    def test_no_changes_when_everything_stable(self):
        self._seed_cart()
        result = store_services.RevalidateCartService(self.customer)
        self.assertEqual(result['changes'], [])
        self.assertFalse(result['blocked'])

    def test_price_change_detected(self):
        self._seed_cart()
        self.product.price = 200000
        self.product.save()
        result = store_services.RevalidateCartService(self.customer)
        self.assertEqual(len(result['changes']), 1)
        change = result['changes'][0]
        self.assertEqual(change['change_type'], 'price_changed')
        self.assertEqual(change['old_price'], 100000)
        self.assertEqual(change['new_price'], 200000)
        self.assertFalse(result['blocked'])

    def test_displayed_prices_compared_against_live(self):
        # قیمت نمایش‌داده‌شده به مشتری ۱۰۰ هزار بود؛ قیمت زنده تغییر کرده است
        self._seed_cart()
        self.product.price = 250000
        self.product.save()
        result = store_services.RevalidateCartService(
            self.customer, displayed_prices={str(self.product.id): 100000}
        )
        change = result['changes'][0]
        self.assertEqual(change['old_price'], 100000)
        self.assertEqual(change['new_price'], 250000)

    def test_not_orderable_blocks(self):
        self._seed_cart()
        self.product.is_orderable = False
        self.product.save()
        result = store_services.RevalidateCartService(self.customer)
        self.assertTrue(result['blocked'])
        self.assertEqual(result['changes'][0]['change_type'], 'not_orderable')

    def test_unpublished_blocks(self):
        self._seed_cart()
        self.product.is_published = False
        self.product.save()
        result = store_services.RevalidateCartService(self.customer)
        self.assertTrue(result['blocked'])
        self.assertEqual(result['changes'][0]['change_type'], 'not_published')
