from database.models import *
from api.serializers import *
from rest_framework import filters
from rest_framework import generics


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ('barangay', 'province', 'paws', 'status', 'request_date',
                         'delivery_date', 'city', 'street', 'building', 'price',
                         'client', )


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('price', 'transaction', 'pieces', )


class UserProfileFilter(filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ('province', 'city', 'barangay', 'street',
                  'building', 'contact_number')


class LaundryShopFilter(filters.FilterSet):
    class Meta:
        model = LaundryShop
        fields = ('name', 'barangay', 'province', 'city',
                     'street', 'building', )#'services')
