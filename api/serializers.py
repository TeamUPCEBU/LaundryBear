from django.contrib.auth.models import User, Group
from rest_framework import serializers
from database.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('url', 'paws', 'status', 'request_date', 'delivery_date',
                  'province', 'city', 'barangay', 'street', 'building',
                  'price', 'client', 'orders')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('client__username','province', 'city', 'barangay', 'street',
                  'building', 'contact_number')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
