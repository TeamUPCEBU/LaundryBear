from django.contrib.auth.models import User, Group
from django.core import serializers as serial
from database.models import *
from rest_framework import viewsets
from api.serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from client.forms import *
from rest_framework.authtoken import views as rest_views
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.authtoken.views import ObtainAuthToken, APIView

from datetime import datetime

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

    def create(self, request, *args, **kwargs):
        admin = self.user.userprofile
        admin.account_type = 2
        admin.save()
        try:
            data = request.data
            shop = LaundryShop()
            shop.admin = admin
            shop.status = 1
            shop.name = data['name']
            shop.province = data['province']
            shop.city = data['city']
            shop.barangay = data['barangay']
            shop.street = data['street']
            shop.building = data['building']
            shop.contact_number = data['contact_number']
            shop.website = data['website']
            shop.status = data['status']
            shop.days_open = data['days_open']
            shop.opening_time = datetime.strptime(data['opening_time'],
                                                  '%H:%M:%S').time()
            shop.closing_time = datetime.strptime(data['closing_time'],
                                                  '%H:%M:%S').time()
            shop.save()
        except Exception as e:
                k = str(e)[1:len(str(e))-1]
                return Response({k:'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        for d_service in data['services']:
            try:
                service = Service(name=d_service['services'], price=d_service['price'])
                service.description = d_service['description']
                service.laundry_shop = shop
                service.save()
            except Exception as e:
                shop.delete()
                k = str(e)[1:len(str(e))-1]
                return Response({k:'This field is required'}, status=status.HTTP_400_BAD_REQUEST)


class ActiveLaundryShopViewSet(LaundryShopViewSet):
    def get_queryset(self):
        return LaundryShop.objects.filter(status=2)


class NearbyLaundryShopViewSet(LaundryShopViewSet):
    def get_queryset(self):
        return LaundryShop.objects.filter(
                admin__barangay=self.request.user.userprofile.barangay,
                status=2)


class ActivateLaundryShopView(LaundryShopViewSet):
    def partial_update(self, request, *args, **kwargs):
        data = request.data
        shop = LaundryShop.objects.get(id=data['id'])
        shop.status = 2
        shop.save()
        shop = self.serializer_class(shop).data
        return Response(shop)


class DeactivateLaundryShopView(LaundryShopViewSet):
    def partial_update(self, request, *args, **kwargs):
        data = request.data
        shop = LaundryShop.objects.get(id=data['id'])
        shop.status = 3
        shop.save()
        shop = self.serializer_class(shop).data
        return Response(shop)


class RejectLaundryShopRequestView(LaundryShopViewSet):
    def partial_update(self, request, *args, **kwargs):
        data = request.data
        shop = LaundryShop.objects.get(id=data['id'])
        shop.status = 4
        shop = self.serializer_class(shop).data
        return Response(shop)


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


    def create(self, request, *args, **kwargs):
        data = request.data
        resp = super(TransactionViewSet, self).create(request, *args, **kwargs)

        transaction = Transaction.objects.get(id=resp.data['id'])
        for d_order in data['orders']:
            try:
                order = Order()
                s = d_order['service']
                order.service = Service.objects.get(id=s['id'])
                order.transaction = transaction
                order.pieces = d_order['pieces']
                order.save()
            except Exception as e:
                transaction.delete()
                k = str(e)[1:len(str(e))-1]
                return Response({k:'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        struct = self.serializer_class(transaction).data
        return Response(struct)


    def update(self, request, *args, **kwargs):
        data = request.data
        resp = super(TransactionViewSet, self).update(request, *args, **kwargs)

        transaction = Transaction.objects.get(id=resp.data['id'])
        for d_order in data['orders']:
            try:
                order = Order()
                s = d_order['service']
                order.service = Service.objects.get(id=s['id'])
                order.transaction = transaction
                order.pieces = d_order['pieces']
                order.save()
            except Exception as e:
                transaction.delete()
                k = str(e)[1:len(str(e))-1]
                return Response({k:'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        struct = self.serializer_class(transaction).data
        return Response(struct)


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


class SignUpUserViewSet(generics.CreateAPIView):
    def post(self, request):
        return super(SignUpUserViewSet, self).post(request)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CreateProfileViewSet(generics.CreateAPIView):
    def post(self, request):
        return super(CreateProfileViewSet, self).create(request)


class CustomerUserProfileViewSet(UserProfileViewSet):
    def get_queryset(self):
        return UserProfile.objects.filter(account_type=1)


class ShopAdminUserProfileViewSet(UserProfileViewSet):
    def get_queryset(self):
        return UserProfile.objects.filter(account_type=2)


class LaundryBearAdminUserProfileViewSet(UserProfileViewSet):
    def get_queryset(self):
        return UserProfile.objects.filter(account_type=3)


class MyCustomersViewSet(UserProfileViewSet):
    def get_queryset(self):
        shop = self.request.user.userprofile.laundry_shop
        t = Transaction.objects.filter(
                    orders__service__laundry_shop=shop)
        return UserProfile.objects.filter(transactions__in=t).distinct()


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
        context['token'] = 'Token ' + token.key
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
