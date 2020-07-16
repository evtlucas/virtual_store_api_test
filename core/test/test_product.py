from django.test import TestCase
from django.db.utils import IntegrityError

from core.models import Product


class TestProduct(TestCase):

    def test_product_well_defined(self):
        product_sku = 1
        product = Product(sku_id=product_sku, description='Butter', price=1.0)
        product.save()
        product_test = Product.objects.get(sku_id=product_sku)
        assert product_test.description == product.description
        assert product_test.price == product.price

    def test_do_not_allow_null_description(self):
        try:
            Product(sku_id=2, description=None, price=1.0).save()
        except IntegrityError:
            pass
