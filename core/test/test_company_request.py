from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Company

from .setup_user import SetupUser


class TestCompanyRequest(APITestCase):
    fixtures = ['customers.yaml']

    def setUp(self):
        self.url = reverse('companies')
        self.new_pk = 3
        self.data = {
            'name': 'ABC',
            'address':
            'Rua Z, n. 2',
            'city': 'São Paulo',
            'state': 'SP',
            'country': 'Brazil',
            'phone_number': '(11) 1234-5678',
            'cnpj': '0123456789123',
            'doing_business_as': 'ABC'
        }
        self.token = SetupUser.get_token()

    def test_create_company(self):
        number_of_companies = Company.objects.count()
        response = self.client.post(
            self.url,
            self.data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), number_of_companies + 1)
        self.assertEqual(Company.objects.get(pk=self.new_pk).name, self.data['name'])

    def test_update_company(self):
        pk=2
        response = self.client.put(
            '/companies/{}/'.format(pk),
            self.data,
            format='json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=pk).name, self.data['name'])

    def test_delete_company(self):
        number_of_companies = Company.objects.count()
        data = {'pk': 2}
        details_url = reverse('company', kwargs=data)
        response = self.client.delete(
            details_url,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), number_of_companies - 1)