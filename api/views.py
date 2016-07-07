from django.contrib.auth.models import User, Group
from database.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.authtoken import views as rest_views
from django.views.decorators.csrf import *

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


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


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

@csrf_exempt
def obtain_auth_token(request):
    print request.POST
    return rest_views.obtain_auth_token(request)
