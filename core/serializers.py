from rest_framework import serializers

from .models import Product, Person, Company, Customer


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