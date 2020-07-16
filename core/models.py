from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MinLengthValidator
from model_utils.managers import InheritanceManager


class Product(models.Model):
    sku_id = models.CharField(max_length=13, unique=True)
    description = models.CharField(max_length=200, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10,
        validators=[MinValueValidator(Decimal('0.01'))])


class Customer(models.Model):
    PERSON = 'person'
    COMPANY = 'company'

    objects = InheritanceManager()

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)

    def type(self):
        try:
            if self.person:
                return self.PERSON
        except:
            if self.company:
                return self.COMPANY

    @classmethod
    def get_child(self, pk, type):
        return Customer.objects.select_subclasses(type).filter(pk=pk)[0]


class Person(Customer):
    cpf = models.CharField(max_length=11, unique=True)


class Company(Customer):
    cnpj = models.CharField(max_length=14, unique=True)
    doing_business_as = models.CharField(max_length=50)
