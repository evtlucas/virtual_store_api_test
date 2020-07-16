from django.test import TestCase

from core.models import Customer, Person, Company


class TestCustomer(TestCase):
    fixtures = ['customers.yaml']

    def test_verify_number_customers(self):
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Company.objects.count(), 1)

    def test_verify_correct_category_name_person(self):
        pk_person = 1
        customer = Customer.objects.get(pk=pk_person)
        person = Person.objects.get(pk=pk_person)
        customer_with_subclass = Customer.get_child(pk_person, customer.type())
        self.assertEqual(customer.type(), Customer.PERSON)
        self.assertEqual(customer_with_subclass.cpf, person.cpf)

    def test_verify_correct_category_name_company(self):
        pk_company = 2
        customer = Customer.objects.get(pk=pk_company)
        company = Company.objects.get(pk=pk_company)
        customer_with_subclass = Customer.get_child(pk_company, customer.type())
        self.assertEqual(customer.type(), Customer.COMPANY)
        self.assertEqual(customer_with_subclass.cnpj, company.cnpj)
        self.assertEqual(customer_with_subclass.doing_business_as, company.doing_business_as)
