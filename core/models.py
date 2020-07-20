import datetime

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MinLengthValidator
from model_utils.managers import InheritanceManager


class Product(models.Model):
    """Model designed to store specific data about products."""
    sku_id = models.CharField(max_length=13, unique=True)
    description = models.CharField(max_length=200, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10,
        validators=[MinValueValidator(Decimal('0.01'))])


class Customer(models.Model):
    """
    Model designed to store specific data about customers in general.
    InheritanceManager is useful to get the subclasses of Customer.
    """
    class Meta:
        ordering = ['id']

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
    """
    Model designed for hold specific data about humans. This class is inherited from customer.
    """
    cpf = models.CharField(max_length=11, unique=True)


class Company(Customer):
    """
    Model designed for hold specific data about companies. This class is inherited from customer.
    """
    cnpj = models.CharField(max_length=14, unique=True)
    doing_business_as = models.CharField(max_length=50)


class Order(models.Model):
    """
    Model designed to store specific data about orders. It has a relationship between customer.
    """
    order_date = models.DateField(null=False, blank=False)
    ship_date = models.DateField(null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delivery_address = models.CharField(max_length=100)
    delivery_city = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=2)
    delivery_country = models.CharField(max_length=20)
    delivery_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return "{} - {}".format(self.customer.name, self.order_date.strftime('%d/%m/%Y'))


class OrderItem(models.Model):
    """
    Model designed to store data about the items sold in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    sku_id = models.CharField(max_length=13, unique=True)
    description = models.CharField(max_length=200, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10,
        validators=[MinValueValidator(Decimal('0.01'))])
    quantity = models.DecimalField(decimal_places=3, max_digits=6,
        default=Decimal('1.000'))

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.description
