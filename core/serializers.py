from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Product
from .models import Order, OrderItem
from .models import Person, Company, Customer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku_id', 'description', 'price']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CustomerSerializer(serializers.BaseSerializer):
    """
    This method is modified from its ancestor in order to return the customer type.
    The customer type might help to get the information about the inherited type of the customer.
    """
    def to_representation(self, instance):
        return {
            'pk': instance.id,
            'name': instance.name,
            'address': instance.address,
            'city': instance.city,
            'state': instance.state,
            'country': instance.country,
            'phone_number': instance.phone_number,
            'customer_type': instance.type()
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False, read_only=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'order_date',
            'ship_date',
            'delivery_address',
            'delivery_city',
            'delivery_state',
            'delivery_country',
            'delivery_phone_number',
            'order_items'
        ]

    def to_internal_value(self, data):
        return {
            'customer': data['customer'],
            'order_date': data['order_date'],
            'ship_date': data['ship_date'],
            'delivery_address': data['delivery_address'],
            'delivery_city': data['delivery_city'],
            'delivery_state': data['delivery_state'],
            'delivery_country': data['delivery_country'],
            'delivery_phone_number': data['delivery_phone_number'],
            'order_items': data['order_items']
        }

    def create(self, validated_data):
        customer_data = validated_data['customer']
        order_items_data = validated_data['order_items']
        order = Order(
            customer_id=customer_data['pk'],
            order_date=validated_data['order_date'],
            ship_date=validated_data['ship_date'],
            delivery_address=validated_data['delivery_address'],
            delivery_city=validated_data['delivery_city'],
            delivery_state=validated_data['delivery_state'],
            delivery_country=validated_data['delivery_country'],
            delivery_phone_number=validated_data['delivery_phone_number']
        )
        order.save()
        self.save_order_items(order, order_items_data)
        return order

    def update(self, instance, validated_data):
        customer_data = validated_data['customer']
        order_items_data = validated_data['order_items']
        instance.customer_id = customer_data['pk']
        instance.order_date = validated_data['order_date']
        instance.ship_date = validated_data['ship_date']
        instance.delivery_address = validated_data['delivery_address']
        instance.delivery_city = validated_data['delivery_city']
        instance.delivery_state=validated_data['delivery_state']
        instance.delivery_country = validated_data['delivery_country']
        instance.delivery_phone_number = validated_data['delivery_phone_number']
        instance.save()
        self.save_order_items(instance, order_items_data)
        return instance

    def save_order_items(self, order, order_items_data):
        for item in order_items_data:
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                sku_id=item['sku_id'],
                description=item['description'],
                price=item['price'],
                quantity=item['quantity']
            )
            order_item.save()



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
