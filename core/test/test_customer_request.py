from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Customer


class TestCustomerRequest(APITestCase):
    fixtures = ['customers.yaml']

    def test_customer_list_with_types(self):
        url = reverse('customers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['customer_type'], Customer.PERSON)
        self.assertEqual(response.data[1]['customer_type'], Customer.COMPANY)