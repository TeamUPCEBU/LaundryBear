from django.contrib.auth.models import User, Group
from rest_framework import serializers
from database.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name',
                  'first_name', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        depth = 2
        fields = ('id', 'name', 'description', 'price')


class LaundryShopSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = LaundryShop
        depth = 1
        fields = ('id', 'name', 'province', 'city', 'barangay', 'street',
                  'building', 'contact_number', 'website',
                  'opening_time', 'closing_time', 'services')

class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'service', 'transaction','pieces')


class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = ('id', 'delivery_fee', 'service_charge', 'name')


class TransactionSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Transaction
        fields = ('id', 'paws', 'status', 'request_date', 'delivery_date',
                  'province', 'city', 'barangay', 'street', 'building',
                  'price', 'client', 'orders', 'fee')


class UserProfileSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'client', 'province', 'city', 'barangay', 'street',
                  'building', 'contact_number')
