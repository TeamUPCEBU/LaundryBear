from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^menu$', views.LaundryMenuView.as_view(), name='menu'),
    url(r'^login$', views.AdminLoginView.as_view(), name='login-admin'),
    url(r'^logout$', views.AdminLogoutView.as_view(), name='logout-admin'),
]
