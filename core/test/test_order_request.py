from datetime import date
from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Order, OrderItem, Customer
from core.serializers import CustomerSerializer


class TestOrderRequest(APITestCase):
    fixtures = ['customers.yaml', 'orders.yaml']

    def test_create_order(self):
        pk = 2
        number_of_orders = Order.objects.count()
        url = reverse('orders')
        customer_data = CustomerSerializer(Customer.objects.get(pk=1)).data
        data = {
            'pk': pk,
            'customer': customer_data,
            'order_date': date(2020, 7, 16),
            'ship_date': date(2020, 7, 16),
            'delivery_address': 'X',
            'delivery_city': 'Y',
            'delivery_state': 'SP',
            'delivery_country': 'BR',
            'delivery_phone_number':
            '1111-1111',
            'order_items': []
        }
        self.client.post(url, data, format='json')
        self.assertEqual(Order.objects.count(), (number_of_orders + 1))
        self.assertEqual(Order.objects.get(pk=pk).customer.id, customer_data['pk'])

    def test_update_order(self):
        pk = 1
        url = reverse('order', kwargs={'pk': pk})
        customer_data = CustomerSerializer(Customer.objects.get(pk=1)).data
        data = {
            'pk': pk,
            'customer': customer_data,
            'order_date': date(2020, 7, 17),
            'ship_date': date(2020, 7, 16),
            'delivery_address': 'X',
            'delivery_city': 'Y',
            'delivery_state': 'SP',
            'delivery_country': 'BR',
            'delivery_phone_number':
            '1111-1111',
            'order_items': []
        }
        self.client.put(url, data, format='json')
        self.assertEqual(Order.objects.get(pk=pk).order_date, data['order_date'])

    def test_delete_order(self):
        pk = 1
        url = reverse('order', kwargs={'pk': pk})
        number_of_orders = Order.objects.count()
        self.client.delete(url)
        self.assertEqual(Order.objects.count(), (number_of_orders - 1))

    def test_insert_order_item_into_order(self):
        pk = 1
        url = reverse('order', kwargs={'pk': pk})
        customer_data = CustomerSerializer(Customer.objects.get(pk=1)).data
        sku_id = 1
        order_item_data = {
            'sku_id': sku_id,
            'description': 'Cake',
            'price': 5.84
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
        self.client.put(url, data, format='json')
        self.assertEqual(Order.objects.get(pk=pk).order_date, data['order_date'])
        order_item = OrderItem.objects.get(order__id=pk, sku_id=sku_id)
        self.assertEqual(order_item.description, order_item_data['description'])
