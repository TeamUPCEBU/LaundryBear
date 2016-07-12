from database.models import *
from api.serializers import *
from rest_framework import filters
from rest_framework import generics
import django_filters


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ('barangay', 'province', 'paws', 'status', 'request_date',
                         'delivery_date', 'city', 'street', 'building', 'price',
                         'client', )


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('transaction', 'pieces', 'service')


class UserProfileFilter(filters.FilterSet):
    email = django_filters.CharFilter(name="user__email")
    class Meta:
        model = UserProfile
        fields = ('province', 'city', 'barangay', 'street',
                  'building', 'contact_number', 'email')


class LaundryShopFilter(filters.FilterSet):
    barangay = django_filters.CharFilter(name="admin__barangay")
    city = django_filters.CharFilter(name="admin__city")
    province = django_filters.CharFilter(name="admin__province")
    street = django_filters.CharFilter(name="admin__street")
    building = django_filters.CharFilter(name="admin__building")
    email = django_filters.CharFilter(name="admin__user__email")

    class Meta:
        model = LaundryShop
        fields = ('name', 'barangay', 'province', 'city',
                     'street', 'building', 'email', )
