from rest_framework import serializers
from .models import *


class OrderBurgerSerializer(serializers.ModelSerializer):
    get_total = serializers.ReadOnlyField()
    get_burger = serializers.ReadOnlyField()
    get_customer = serializers.ReadOnlyField()

    class Meta:
        model = OrderBurger
        fields = '__all__'


class BurgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Burger
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    get_cart_total = serializers.ReadOnlyField()
    get_cart_burgers = serializers.ReadOnlyField()
    shipping = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
