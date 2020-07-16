from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Person


class TestPersonRequest(APITestCase):
    fixtures = ['customers.yaml']

    def setUp(self):
        self.url = reverse('people')
        self.new_pk = 3

    def test_create_person(self):
        number_of_people = Person.objects.count()
        data = {
            'name': 'Ciclano',
            'address':
            'Rua Z, n. 2',
            'city': 'São Paulo',
            'state': 'SP',
            'country': 'Brazil',
            'phone_number': '(11) 1234-5678',
            'cpf': '12345678901'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), number_of_people + 1)
        self.assertEqual(Person.objects.get(pk=self.new_pk).name, data['name'])

    def test_update_product(self):
        pk=1
        data = {
            'name': 'Ciclano',
            'address':
            'Rua Z, n. 2',
            'city': 'São Paulo',
            'state': 'SP',
            'country': 'Brazil',
            'phone_number': '(11) 1234-5678',
            'cpf': '12345678901'
        }
        response = self.client.put('/person/{}/'.format(pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Person.objects.get(pk=pk).name, data['name'])

    def test_delete_product(self):
        number_of_people = Person.objects.count()
        data = {'pk': 1}
        details_url = reverse('person', kwargs=data)
        response = self.client.delete(details_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), number_of_people - 1)