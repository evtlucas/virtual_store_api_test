from datetime import date
from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Order, OrderItem, Customer
from core.serializers import CustomerSerializer

from .setup_user import SetupUser


class TestOrderItemRequest(APITestCase):
    fixtures = ['customers.yaml', 'orders.yaml', 'order_items.yaml']

    def setUp(self):
        self.token = SetupUser.get_token()

    def test_insert_order_item_into_order(self):
        pk = 1
        url = reverse('order', kwargs={'pk': pk})
        customer_data = CustomerSerializer(Customer.objects.get(pk=1)).data
        sku_id = 2
        order_item_data = {
            'sku_id': sku_id,
            'description': 'Cake',
            'price': Decimal('5.84'),
            'quantity': 2
        }
        data = {
            'pk': pk,
            'customer': customer_data,
            'order_date': date(2020, 7, 17),
            'ship_date': date(2020, 7, 16),
            'delivery_address': 'X',
            'delivery_city': 'Y',
            'delivery_state': 'SP',
            'delivery_country': 'BR',
            'delivery_phone_number': '1111-1111',
            'order_items': [order_item_data]
        }
        self.client.put(
            url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        saved_order = Order.objects.get(pk=pk)
        self.assertEqual(saved_order.order_date, data['order_date'])
        filtered_items = OrderItem.objects.filter(order_id=pk, sku_id=sku_id)
        self.assertGreater(len(filtered_items), 0)
        order_item = filtered_items[0]
        self.assertEqual(order_item.description, order_item_data['description'])
        self.assertEqual(order_item.quantity, order_item_data['quantity'])

    def test_insert_order_item_into_order_using_url(self):
        pk = 1
        sku_id = 2
        url = reverse('order_items', kwargs={'order_pk': pk})
        order_item_data = {
            'order': pk,
            'sku_id': sku_id,
            'description': 'Cake',
            'price': Decimal('5.84'),
            'quantity': 2
        }
        self.client.post(
            url,
            order_item_data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        filtered_items = OrderItem.objects.filter(order_id=pk, sku_id=sku_id)
        self.assertGreater(len(filtered_items), 0)
        order_item = filtered_items[0]
        self.assertEqual(order_item.description, order_item_data['description'])
        self.assertEqual(order_item.quantity, order_item_data['quantity'])

    def test_update_order_item_url(self):
        pk = 2
        item_pk = 2
        url = reverse('order_item_detail', kwargs={'order_pk': pk, 'pk': item_pk})
        order_item_data = {
            'order': pk,
            'sku_id': item_pk,
            'description': 'Bucket',
            'price': Decimal('10.99'),
            'quantity': 1
        }
        self.client.put(
            url,
            order_item_data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        filtered_items = OrderItem.objects.filter(order_id=pk, id=item_pk)
        self.assertGreater(len(filtered_items), 0)
        order_item = filtered_items[0]
        self.assertEqual(order_item.description, order_item_data['description'])
        self.assertEqual(order_item.price, order_item_data['price'])
        self.assertEqual(order_item.quantity, order_item_data['quantity'])
        calculated_total_price = order_item_data['price'] * order_item_data['quantity']
        self.assertEqual(order_item.total_price, calculated_total_price)

    def test_delete_order_item_url(self):
        pk = 2
        item_pk = 2
        url = reverse('order_item_detail', kwargs={'order_pk': pk, 'pk': item_pk})
        self.client.delete(url, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        filtered_items = OrderItem.objects.filter(order_id=pk, id=item_pk)
        self.assertEqual(len(filtered_items), 0)