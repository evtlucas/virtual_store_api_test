from django.utils.decorators import method_decorator

from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from .models import Product, Person, Company, Customer, Order
from .serializers import ProductSerializer, PersonSerializer
from .serializers import CompanySerializer, CustomerSerializer
from .serializers import OrderSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all products sold by the retailer."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of a product."
))
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retrieve a simple product by its id."
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Allows the update of a product."
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Removes a product from the database."
))
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all customers that are people."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of a person."
))
class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retrieve a simple person by its id."
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Allows the update of a person."
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Removes a person from the database."
))
class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all customers that are companies."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of a company."
))
class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retrieve a simple company by its id."
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Allows the update of a company."
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Removes a person from the database."
))
class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all customers that are either people or companies."
))
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all orders."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of an order."
))
class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retrieve a order company by its id."
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Allows the update of an order."
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Removes an order from the database. It's made by the order id."
))
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
