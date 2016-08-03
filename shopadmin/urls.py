from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

from shopadmin import views

#Urls used for client side
#Needs: RegEx, View to inherit, Name
#RegEx: r'^(name of url)$
#View: Which view to show
#Name: Used in views and template tags
urlpatterns = [
    url(r'^promos$', views.ReloadCreditsandPromoView.as_view(), name='promos'),
    url(r'^thanks$', views.PendingRegNoticeView.as_view(), name='pending-registration'),
    url(r'^menu$', views.LaundryMenuView.as_view(), name='menu'),
    url(r'^shops/add$', views.LaundryCreateView.as_view(), name='add-shop'),
    #url(r'^shops/edit/(?P<pk>\d+)$', views.LaundryUpdateView.as_view(),
    #    name='edit-shop'),
    url(r'^shops/list$', views.LaundryListView.as_view(), name='list-shops'),
    url(r'^shops/delete/(?P<pk>\d+)$', views.LaundryDeleteView.as_view(),
        name='delete-shop'),
    # url(r'^login$', views.ShopAdminLoginView.as_view(), name='login-admin'),
    url(r'^logout$', views.ShopAdminLogoutView.as_view(), name='logout-admin'),
    url(r'^clients/list$', views.ClientListView.as_view(), name='list-client'),
    url(r'^settings$', views.AdminSettingsView.as_view(), name='settings'),
    url(r'^services/list$', views.ServicesListView.as_view(),
        name='list-service'),
    url(r'^services/delete/(?P<pk>\d+)$', views.ServicesDeleteView.as_view(),
        name='delete-service'),
    url(r'^services/add$', views.ServiceCreateView.as_view(),
        name='create-service'),
    url(r'^services/edit/(?P<pk>\d+)$', views.ServiceUpdateView.as_view(),
        name='edit-service'),
    url(r'^service/add$', views.AddNewServiceView.as_view(), name='add-service'),
    url(r'^transactions/pending$', views.PendingRequestedTransactionsView.as_view(), name='pending-transactions'),
    url(r'^transactions/ongoing$', views.OngoingTransactionsView.as_view(), name='ongoing-transactions'),
    url(r'^transactions/history$', views.HistoryTransactionsView.as_view(), name='history-transactions'),
    url(r'^transactions/update/(?P<pk>\d+)$', views.UpdateTransactionDeliveryDateView.as_view(), name='update-transaction'),
    url(r'^transactions/ongoing/(?P<pk>\d+)/done$', views.MarkTransactionDoneView.as_view(), name='mark-transaction-done'),
]
