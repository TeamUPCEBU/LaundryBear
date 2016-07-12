from django.contrib.auth.models import User, Group
from django.core import serializers
from database.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.authtoken import views as rest_views
from rest_framework import filters
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken

from api.models import *

import json

################# Shops #################

class LaundryShopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shops to be viewed or edited.
    """
    queryset = LaundryShop.objects.all()
    serializer_class = LaundryShopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    fields = ('name', 'barangay', 'province', 'city',
                     'street', 'building', 'the_services')



class ActiveLaundryShopViewSet(LaundryShopViewSet):
    def get_queryset(self):
        return LaundryShop.objects.filter(status=2)



class NearbyLaundryShopViewSet(LaundryShopViewSet):
    def get_queryset(self):
        return LaundryShop.objects.filter(
                admin__barangay=self.request.user.userprofile.barangay,
                status=2)



################# Transactions #################

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('barangay', 'province', 'paws', 'status', 'request_date',
                     'delivery_date', 'city', 'street', 'building', 'price',
                     'client')


class ClientTransactionViewSet(TransactionViewSet):
    def get_queryset(self):
        return self.request.user.userprofile.transactions.all()


class ShopTransactionViewSet(TransactionViewSet):
    def get_queryset(self):
        admin = self.request.user.userprofile
        return Transaction.objects.filter(
                orders__service__laundry_shop=admin.laundry_shop)



class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


################# Users #################

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomerUserProfileViewSet(UserProfileViewSet):
    def get_queryset(self):
        return UserProfile.objects.filter(account_type=1)

class ShopAdminUserProfileViewSet(UserProfileViewSet):
    def get_queryset(self):
        return UserProfile.objects.filter(account_type=2)


class LaundryBearAdminUserProfileViewSet(UserProfileViewSet):
    def get_queryset(self):
        return UserProfile.objects.filter(account_type=3)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GetAuthToken(ObtainAuthToken):
    #@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ObtainAuthToken, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print user.userprofile
        context = {}
        context['token'] = token.key
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['email'] = user.email
        context['province'] = user.userprofile.province
        context['city'] = user.userprofile.city
        context['barangay'] = user.userprofile.barangay
        context['street'] = user.userprofile.street
        context['building'] = user.userprofile.building
        context['contact_number'] = user.userprofile.contact_number
        context['id'] = user.userprofile.id
        return Response(context)
