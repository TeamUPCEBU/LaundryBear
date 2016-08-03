import json

from database.models import LaundryShop, Price, Service, UserProfile, Transaction, Order, Fees, ReloadRequest

from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, FormView, ListView,
                                  RedirectView, TemplateView, UpdateView)

from shopadmin import forms
from shopadmin.mixins import ShopAdminLoginRequiredMixin
from LaundryBear.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from database.models import LaundryShop, UserProfile
#Django uses class based views to connect with templates.
#Each class based view has their own methods.
#You can still add more methods if needed.
#Check ccbv.co.uk for more information


class ReloadCreditsandPromoView(ShopAdminLoginRequiredMixin, CreateView):
    template_name ='shopadmin/account/promos.html'
    model = ReloadRequest
    form_class = forms.ReloadForm

    def get_success_url(self):
        """
        Redirect to the list of shops if laundry shop creation was a success.
        """
        return reverse('shopadmin:menu')


class PendingRegNoticeView(ShopAdminLoginRequiredMixin, TemplateView):
    template_name = 'shopadmin/account/confirmation.html'

    def get(self, request, *args, **kwargs):
        try:
            shop = self.request.user.userprofile.laundry_shop
            if shop.status == LaundryShop.ACTIVE and shop.credits > 0:
                return redirect('shopadmin:menu')
            else:
                return super(PendingRegNoticeView, self).get(request, *args, **kwargs)
        except Exception as e:
            return redirect('shopadmin:add-shop')

class LaundryMenuView(ShopAdminLoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'pending_transaction_list'
    template_name = 'shopadmin/shop/laundrybearmenu.html'

    def get_queryset(self):
        queryset = super(LaundryMenuView, self).get_queryset()
        queryset = queryset.filter(status=1,
                order__price__laundry_shop=self.request.user.userprofile.laundry_shop).order_by('request_date')[:3]
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            shop = self.request.user.userprofile.laundry_shop
            if (shop.status == LaundryShop.PENDING or
                shop.status == LaundryShop.INACTIVE or
                shop.status == LaundryShop.REJECTED or
                shop.credits == 0):
                return redirect('shopadmin:pending-registration')
            else:
                return super(LaundryMenuView, self).get(request, *args, **kwargs)
        except Exception as e:
            return redirect('shopadmin:add-shop')


class LaundryCreateView(ShopAdminLoginRequiredMixin, CreateView):
    """
    View to create a laundry shop. Takes user input and creates and saves a
    laundry shop into the database.
    """
    template_name = 'shopadmin/shop/addlaundryshop.html'
    model = LaundryShop
    form_class = forms.LaundryShopForm

    def get_success_url(self):
        """
        Redirect to the list of shops if laundry shop creation was a success.
        """
        return reverse('shopadmin:list-shops')

    def form_valid(self, form):
        """
        Save the laundry shop when form is valid, along with related objects.
        """
        # 'admin', 'status',
        data = self.request.POST

        response = super(LaundryCreateView, self).form_valid(form)
        PriceInlineFormSet = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price', 'duration'), extra=1)
        price_formset = PriceInlineFormSet(
            data=data, instance=self.object)
        if price_formset.is_valid():
            price_formset.save()
        else:
            print price_formset.errors
        return response

    def get_context_data(self,**kwargs):
        context = super(LaundryCreateView, self).get_context_data(**kwargs)
        context['service_list'] = Service.objects.all().order_by('pk')
        price_formset = inlineformset_factory(
            LaundryShop, Price, fields=('service', 'price', 'duration'), extra=1)
        context['price_formset'] = price_formset()
        return context


class LaundryListView(ShopAdminLoginRequiredMixin, ListView):
    """
    A view that lists at most 10 laundry shops in a page.
    Also allows filtering.
    """
    model = LaundryShop
    paginate_by = 10
    ordering = 'name'
    template_name = 'shopadmin/shop/viewlaundryshops.html'
    context_object_name = 'shop_list'

    def get_context_data(self, **kwargs):
        """
        Filter laundry shop to display by a query.
        Allow querying by laundry shop name, city, province, or barangay.
        """
        context = super(LaundryListView, self).get_context_data(**kwargs)
        shops = context['shop_list']
        name_query = self.request.GET.get('name', False)

        query_type = 'name'
        if name_query:
            shops = self.get_shops_by_name(name_query)
            query_type = 'name'
        city_query = self.request.GET.get('city', False)
        if city_query:
            shops = self.get_shops_by_city(city_query)
            query_type = 'city'
        province_query = self.request.GET.get('province', False)
        if province_query:
            shops = self.get_shops_by_province(province_query)
            query_type = 'province'
        barangay_query = self.request.GET.get('barangay', False)
        if barangay_query:
            shops = self.get_shops_by_barangay(barangay_query)
            query_type = 'barangay'
        context.update({'shop_list': shops})
        context['query_type'] = query_type
        return context

    def get_shops_by_name(self, name_query):
        return LaundryShop.objects.filter(name__icontains=name_query)

    def get_shops_by_city(self, city_query):
        return LaundryShop.objects.filter(city__icontains=city_query)

    def get_shops_by_province(self, province_query):
        return LaundryShop.objects.filter(province__icontains=province_query)

    def get_shops_by_barangay(self, barangay_query):
        return LaundryShop.objects.filter(barangay__icontains=barangay_query)


class LaundryDeleteView(ShopAdminLoginRequiredMixin, DeleteView):
    """ A view to delete a laundry shop. """
    model = LaundryShop

    def get_success_url(self):
        return reverse('shopadmin:list-shops')


class ShopAdminLogoutView(LogoutView):
    """ A view that logs out the user and redirects to the admin login. """
    login_view_name = 'client:login'


class ClientListView(ShopAdminLoginRequiredMixin, ListView):
    """ A view that shows a list of clients. Also filterable. """
    model = UserProfile
    paginate_by = 10
    template_name = 'shopadmin/client/viewclients.html'
    context_object_name = 'user_list'
    ordering = ['user__first_name', 'user__last_name']

    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()
        return queryset.filter(
                        transactions__order__price__laundry_shop=
                        self.request.user.userprofile.laundry_shop).distinct()

    def get_context_data(self, **kwargs):
        """
        Filters the list of clients to return.
        Filters by client name, city, province, or barangay.
        """
        context = super(ClientListView, self).get_context_data(**kwargs)
        client = context['user_list']

        name_query = self.request.GET.get('name', False)
        query_type = 'name'
        if name_query:
            client = self.get_user_by_name(name_query)
            query_type = 'name'
        city_query = self.request.GET.get('city', False)
        if city_query:
            client = self.get_user_by_city(city_query)
            query_type = 'city'
        province_query = self.request.GET.get('province', False)
        if province_query:
            client = self.get_user_by_province(province_query)
            query_type = 'province'
        barangay_query = self.request.GET.get('barangay', False)
        if barangay_query:
            client = self.get_user_by_barangay(barangay_query)
            query_type = 'barangay'
        context.update({'user_list': client})
        context['query_type'] = query_type
        return context

    def get_user_by_name(self, name_query):
        return UserProfile.objects.filter((Q(user__first_name__icontains=name_query)|
                                          Q(user__last_name__icontains=name_query)))

    def get_user_by_city(self, city_query):
        return UserProfile.objects.filter(city__icontains=city_query)

    def get_user_by_province(self, province_query):
        return UserProfile.objects.filter(province__icontains=province_query)

    def get_user_by_barangay(self, barangay_query):
        return UserProfile.objects.filter(barangay__icontains=barangay_query)


class ServicesListView(ShopAdminLoginRequiredMixin, ListView):
    """ A view to show the list of services. """
    model = Service
    paginate_by = 10
    template_name = 'shopadmin/shop/viewservices.html'
    context_object_name = 'service_list'

    def get_context_data(self, **kwargs):
        """ Filters list to show service name or description. """
        context = super(ServicesListView, self).get_context_data(**kwargs)
        service = context['service_list']

        name_query = self.request.GET.get('name', False)
        query_type = 'name'
        if name_query:
            service = self.get_service_by_name(name_query)
            query_type = 'name'
        description_query = self.request.GET.get('description', False)
        if description_query:
            service = self.get_service_by_description(description_query)
            query_type = 'description'

        context.update({'service_list': service})
        context['query_type'] = query_type
        return context

    def get_service_by_name(self, name_query):
        return Service.objects.filter(name__icontains=name_query)

    def get_service_by_description(self, description_query):
        return Service.objects.filter(description__icontains=description_query)

class ServicesDeleteView(ShopAdminLoginRequiredMixin, DeleteView):
    """ A view to delete a service. """
    model = Service

    def get_success_url(self):
        return reverse('shopadmin:list-service')


class ServiceCreateView(ShopAdminLoginRequiredMixin, CreateView):
    """ A view to create a service through JS AJAX. Returns JSON. """
    template_name = 'shopadmin/shop/partials/createservice.html'
    model = Service
    form_class = forms.ServiceForm

    def post(self, request, *args, **kwargs):
        response = super(ServiceCreateView, self).post(request, *args, **kwargs)
        if self.object:
            service = {}
            service['name'] = self.object.name
            service['description'] = self.object.description
            service['pk'] = self.object.pk
            # return a JSON string as a response
            return HttpResponse(json.dumps(service))
        else:
            return response

    def get_success_url(self):
        return reverse('shopadmin:create-service')


class ServiceUpdateView(ShopAdminLoginRequiredMixin, UpdateView):
    """ A view to update a service. """
    template_name = 'shopadmin/shop/editservices.html'
    model = Service
    form_class = forms.ServiceForm

    def get_success_url(self):
        return reverse('shopadmin:list-service')


class AddNewServiceView(ShopAdminLoginRequiredMixin, CreateView):
    """ A view to add a new service. (non-ajax) """
    template_name = 'shopadmin/shop/addnewservice.html'
    model = Service
    form_class = forms.ServiceForm

    def get_success_url(self):
        return reverse('shopadmin:list-service')


class PendingRequestedTransactionsView(ShopAdminLoginRequiredMixin, ListView):
    """ A view to show pending transactions. """
    model = Transaction
    context_object_name = 'pending_transaction_list'
    template_name = 'shopadmin/transactions/pending_requested_transactions.html'
    paginate_by = 10

    def get_queryset(self):
        """ Filters the set of transactions to only pending ones. """
        queryset = super(PendingRequestedTransactionsView, self).get_queryset()
        queryset = queryset.filter(status=1, order__price__laundry_shop=self.request.user.userprofile.laundry_shop)

        return queryset


class OngoingTransactionsView(ShopAdminLoginRequiredMixin, ListView):
    """ A view to show ongoing transactions. """
    model = Transaction
    context_object_name = 'ongoing_transaction_list'
    template_name = 'shopadmin/transactions/ongoing_transactions.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OngoingTransactionsView,self).get_context_data(**kwargs)
        form_list = []
        for transaction in self.object_list:
            form_list.append(forms.TransactionPriceForm(prefix=transaction.pk, data=self.request.POST or None, instance=transaction))

        context['transaction_list'] = zip(self.object_list, form_list)
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        form_list = context['transaction_list']
        # update the price of the transaction, if updated
        for transaction, form in form_list:
            if form.is_valid():
                form.save()

        return redirect('shopadmin:ongoing-transactions')


    def get_queryset(self):
        """ Filters the set of transactions to only ongoing ones. """
        queryset = super(OngoingTransactionsView, self).get_queryset()
        queryset = queryset.filter(status=2, order__price__laundry_shop=self.request.user.userprofile.laundry_shop)

        return queryset


class HistoryTransactionsView(ShopAdminLoginRequiredMixin, ListView):
    """ A view to show the history of transactions (done, rejected). """
    model = Transaction
    context_object_name = 'history_transaction_list'
    template_name = 'shopadmin/transactions/history_transactions.html'
    paginate_by = 10

    def get_queryset(self):
        """ Filter transactions to only show either done or rejected. """
        queryset = super(HistoryTransactionsView, self).get_queryset()
        filters = (3,4)
        queryset = queryset.filter(order__price__laundry_shop=self.request.user.userprofile.laundry_shop, status__in=filters).order_by('request_date').reverse()

        return queryset

    def get_context_data(self, **kwargs):
        """ Filter by transactions by either client name or laundry shop name. """
        context = super(HistoryTransactionsView, self).get_context_data(**kwargs)
        transaction = context['history_transaction_list']

        name_query = self.request.GET.get('client name', False)
        query_type = 'client name'
        if name_query:
            transaction = self.get_transaction_by_name(name_query)
            query_type = 'client name'

        shop_query = self.request.GET.get('laundry shop', False)
        if shop_query:
            transaction = self.get_transaction_by_shop(shop_query)
            query_type = 'laundry shop'

        context.update({'history_transaction_list': transaction})
        context['query_type'] = query_type
        return context

    def get_transaction_by_name(self, name_query):
        return Transaction.objects.filter(Q(client__client__first_name__icontains=name_query)|
                                          Q(client__client__last_name__icontains=name_query))

    def get_transaction_by_shop(self, shop_query):
        return Transaction.objects.filter(order__price__laundry_shop__name__icontains=shop_query)



class UpdateTransactionDeliveryDateView(ShopAdminLoginRequiredMixin, UpdateView):
    """
    A view to update a transaction delivery date.
    Also handle marking a transaction as approved or declined.
    """
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'shopadmin/transactions/update_transaction.html'
    fields = ['delivery_date']

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateTransactionDeliveryDateView, self) \
            .get_context_data(*args, **kwargs)
        # insert dynamic fees into context
        # context['fees'] = Site.objects.get_current().fees
        context['fees'] = Site.objects.get_or_create(domain='laundrybear.pythonanywhere.com')[0].fees
        return context

    def get_success_url(self):
        return reverse('shopadmin:pending-transactions')

    def post(self, request, *args, **kwargs):
        """ Handle approving a transaction or rejecting it. """
        response = super(UpdateTransactionDeliveryDateView, self).post(request, *args, **kwargs)
        if request.POST.get('approve', False):
            self.object.status = 2
            self.object.save()
        else:
            self.object.status = 4
            self.object.save()
        return response


class MarkTransactionDoneView(ShopAdminLoginRequiredMixin, UpdateView):
    """ A view to mark a transaction done. """
    model = Transaction
    fields = ['status']
    template_name = ''

    def get_success_url(self):
        return reverse('shopadmin:ongoing-transactions')

class AdminSettingsView(ShopAdminLoginRequiredMixin, TemplateView):
    """ A view to edit admin settings. (Password, service charges, delivery fees) """
    template_name = 'shopadmin/account/settings.html'

    def get_context_data(self, **kwargs):
        context = super(AdminSettingsView, self).get_context_data(**kwargs)
        context['usernameform'] = forms.ChangeUsernameForm(data=self.request.POST or None, instance=self.request.user)
        context['passwordform'] = PasswordChangeForm(data=self.request.POST or None, user=self.request.user)
        # site = Site.objects.get_current()


        return context

    def post(self,request,*args,**kwargs):
        """ Check each fields to see if they are valid, if so, save it. """
        context = self.get_context_data(*args, **kwargs)
        usernameform = context['usernameform']
        passwordform = context['passwordform']

        if (usernameform.is_valid()):
            usernameform.save()
        else:
            print usernameform.errors

        if passwordform.is_valid():
            passwordform.save()
        else:
            print passwordform.error_messages


        return self.render_to_response(context)
