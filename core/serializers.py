from rest_framework import serializers

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
        fields = ['sku_id', 'description', 'price']


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

    """
    This method intends to return the classes that are related to the order.
    """
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

    """
    This method was overrided in order to save data about the classes related to order.
    """
    def create(self, validated_data):
        customer_data = validated_data['customer']
        order_items_data = validated_data['order_items']
        customer = Customer.objects.get(pk=customer_data['pk'])
        order = Order(
            customer=customer,
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

    """
    This method was overrided in order to save data about the classes related to order.
    """
    def update(self, instance, validated_data):
        customer_data = validated_data['customer']
        order_items_data = validated_data['order_items']
        customer = Customer.objects.get(pk=customer_data['pk'])
        instance.customer = customer
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

    """
    This method saves the items related to the order.
    """
    def save_order_items(self, order, order_items_data):
        for item in order_items_data:
            order_item = OrderItem(
                order=order,
                sku_id=item['sku_id'],
                description=item['description'],
                price=item['price']
            )
            order_item.save()
