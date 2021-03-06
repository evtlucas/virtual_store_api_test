from datetime import date
from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Order, OrderItem, Customer
from core.serializers import CustomerSerializer

from .setup_user import SetupUser


class TestOrderRequest(APITestCase):
    fixtures = ['customers.yaml', 'orders.yaml']

    def setUp(self):
        self.token = SetupUser.get_token()

    def test_create_order(self):
        pk = 2
        number_of_orders = Order.objects.count()
        url = reverse('orders')
        customer_data = CustomerSerializer(Customer.objects.get(pk=2)).data
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
        self.client.post(
            url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
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
        self.client.put(
            url,
            data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(Order.objects.get(pk=pk).order_date, data['order_date'])

    def test_delete_order(self):
        pk = 1
        url = reverse('order', kwargs={'pk': pk})
        number_of_orders = Order.objects.count()
        self.client.delete(
            url,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(Order.objects.count(), (number_of_orders - 1))
