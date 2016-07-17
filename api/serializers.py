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
        fields = ('id', 'name', 'description', )


class LaundryShopSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = LaundryShop
        depth = 1
        fields = ('id', 'name', 'province', 'city', 'barangay', 'street',
                  'building', 'contact_number', 'website', 'status',
                  'days_open', 'opening_time', 'closing_time',
                  'services', 'admin', 'comments', 'raters')


class PriceSerializer(serializers.ModelSerializer):
    laundry_shop = LaundryShopSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Price
        fields = ('id', 'laundry_shop', 'service', 'price', 'duration')



class OrderSerializer(serializers.ModelSerializer):
    price = PriceSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'price', 'transaction','pieces')


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = ('id', 'delivery_fee', 'service_charge', 'name')


class TransactionSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Transaction
        fields = ('id', 'paws', 'status', 'request_date', 'delivery_date',
                  'province', 'city', 'barangay', 'street', 'building',
                  'price', 'client', 'comment', 'fee', 'orders',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'province', 'city', 'barangay', 'street',
                  'building', 'contact_number', 'account_type')
