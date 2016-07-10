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

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken

from api.models import *

import json

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LaundryShopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shops to be viewed or edited.
    """
    queryset = LaundryShop.objects.all()
    serializer_class = LaundryShopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    fields = ('name', 'barangay', 'province', 'city',
                     'street', 'building', 'the_services')#'services')


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

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


#@csrf_exempt
#def obtain_auth_token(request):
#    req = json.loads(request.body)
#    print req['username']
#    print req['password']
#    rest_views.obtain_auth_token(request)
#    return Response(req)

class GetAuthToken(ObtainAuthToken):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ObtainAuthToken, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print user.client
        context = {}
        context['token'] = token.key
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['email'] = user.email
        context['province'] = user.client.province
        context['city'] = user.client.city
        context['barangay'] = user.client.barangay
        context['street'] = user.client.street
        context['building'] = user.client.building
        context['contact_number'] = user.client.contact_number
        context['id'] = user.client.id
        #return Response({'token': token.key, 'name': user})
        return Response(context)
