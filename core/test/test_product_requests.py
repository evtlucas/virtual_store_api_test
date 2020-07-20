from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Product

from .setup_user import SetupUser


class TestProductRequest(APITestCase):
    fixtures = ['products.yaml']

    def setUp(self):
        self.url = reverse('products')
        self.token = SetupUser.get_token()

    def test_create_product(self):
        number_products = Product.objects.count()
        product_description = 'Butter'
        sku_id = 4
        data = {'sku_id': sku_id, 'description': product_description, 'price': 9.99}
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), number_products + 1)
        self.assertEqual(Product.objects.get(sku_id=sku_id).description, product_description)

    def test_create_product_blank_description(self):
        product_description = ''
        data = {'sku_id': 5, 'description': product_description, 'price': 9.99}
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_price_zero(self):
        product_description = 'Rice'
        data = {'sku_id': 6, 'description': product_description, 'price': 0}
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_price_less_than_zero(self):
        product_description = 'Beans'
        data = {'sku_id': 7, 'description': product_description, 'price': -0.01}
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        product_description = 'Meat'
        sku_id = 2
        data = {'sku_id': sku_id, 'description': product_description, 'price': 5.84}
        response = self.client.put(
            '/products/{}/'.format(sku_id),
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(sku_id=sku_id).description, product_description)

    def test_delete_product(self):
        number_products = Product.objects.count()
        data = {'pk': 3}
        details_url = reverse('products_details', kwargs=data)
        response = self.client.delete(
            details_url,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), number_products - 1)


