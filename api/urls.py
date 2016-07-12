from django.conf.urls import include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'clients', views.UserProfileViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'shops', views.LaundryShopViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'services', views.ServiceViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
