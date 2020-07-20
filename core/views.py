from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .models import Product, Person, Company, Customer, Order, OrderItem
from .serializers import ProductSerializer, PersonSerializer
from .serializers import CompanySerializer, CustomerSerializer
from .serializers import OrderSerializer, OrderItemSerializer
from .serializers import UserSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all products sold by the retailer."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of a product."
))
class ProductList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all customers that are people."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of a person."
))
class PersonList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all customers that are companies."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of a company."
))
class CompanyList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all customers that are either people or companies."
))
class CustomerList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all orders."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of an order."
))
class OrderList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retrieve an order company by its id."
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Allows the update of an order."
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Removes an order from the database. It's made by the order id."
))
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="List all order items."
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Allows the creation of an order item."
))
class OrderItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.filter(order_id=self.kwargs["order_pk"])
        return queryset

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retrieve an order item by its id."
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Allows the update of an order."
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Removes an order from the database. It's made by the order id."
))
class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.filter(id=self.kwargs["pk"], order_id=self.kwargs["order_pk"])
        return queryset

@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Operation that only allows user creation."
))
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)