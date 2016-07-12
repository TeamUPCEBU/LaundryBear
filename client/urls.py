from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()

from . import views

#Urls used for client side
#Needs: RegEx, View to inherit, Name
#RegEx: r'^(name of url)$
#View: Which view to show
#Name: Used in views and template tags
urlpatterns = [
    url(r'^login$', views.ClientLoginView.as_view(), name='login'),
    url(r'^logout$', views.ClientLogoutView.as_view(), name='logout'),
    url(r'^signup$', views.SignupView.as_view(), name='signup'),
    url(r'^$', views.DashView.as_view(), name='menu'),
]
