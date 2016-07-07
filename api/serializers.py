from django.contrib.auth.models import User, Group
from rest_framework import serializers
from database.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class LaundryShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LaundryShop


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('url', 'paws', 'status', 'request_date', 'delivery_date',
                  'province', 'city', 'barangay', 'street', 'building',
                  'price', 'client',) #'order')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
