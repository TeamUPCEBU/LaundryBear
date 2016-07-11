from django.contrib.auth.models import User, Group
from rest_framework import serializers
from database.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'last_name',
                  'first_name', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        depth = 2
        fields = ('id', 'name', 'description')


class PriceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Price
        fields = ('laundry_shop', 'id', 'price', 'duration', 'service')


class LaundryShopSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True)
    class Meta:
        model = LaundryShop
        depth = 1
        fields = ('id', 'name', 'province', 'city', 'barangay', 'street',
                  'building', 'contact_number', 'email', 'website',
                  'hours_open', 'days_open', 'prices')


class OrderSerializer(serializers.ModelSerializer):
    price = PriceSerializer()
    class Meta:
        model = Order
        fields = ('price', 'transaction','pieces')


class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = ('delivery_fee', 'service_charge',)


class TransactionSerializer(serializers.ModelSerializer):
    order_set = OrderSerializer(many=True)
    class Meta:
        model = Transaction
        fields = ('url', 'paws', 'status', 'request_date', 'delivery_date',
                  'province', 'city', 'barangay', 'street', 'building',
                  'price', 'client', 'order_set',)


class UserProfileSerializer(serializers.ModelSerializer):
    client = UserSerializer()
    class Meta:
        model = UserProfile
        # depth = 1
        fields = ('client', 'province', 'city', 'barangay', 'street',
                  'building', 'contact_number')
