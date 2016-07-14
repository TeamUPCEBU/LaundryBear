from django.conf.urls import include, url
from rest_framework import routers
from api import views
router = routers.DefaultRouter()

router.register(r'shops/all', views.LaundryShopViewSet)
router.register(r'shops/nearby', views.NearbyLaundryShopViewSet)
router.register(r'activate/shop', views.ActivateLaundryShopView)
router.register(r'deactivate/shop', views.DeactivateLaundryShopView)
router.register(r'rejectrequest/shop', views.RejectLaundryShopRequestView)


router.register(r'transactions', views.TransactionViewSet)
router.register(r'mytransactions', views.ClientTransactionViewSet)
router.register(r'shoptransactions', views.ShopTransactionViewSet)

router.register(r'orders', views.OrderViewSet)
router.register(r'services', views.ServiceViewSet)

router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet)

router.register(r'customers', views.CustomerUserProfileViewSet)
router.register(r'admin/shops', views.ShopAdminUserProfileViewSet)
router.register(r'admins/laundrybear', views.LaundryBearAdminUserProfileViewSet)

router.register(r'mycustomers', views.MyCustomersViewSet)



router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'signup',views.SignUpUserViewSet.as_view()),
    url(r'profile/create', views.CreateProfileViewSet.as_view())
]
