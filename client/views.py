import json

from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.contrib.sites.models import Site
from django.views.generic import (DetailView, ListView, TemplateView, View)
from django.views.decorators.csrf import *
from django.utils.decorators import method_decorator

from client.forms import ProfileForm, UserForm, AddressForm, TransactionForm, ChangeUsernameForm

from django.contrib.auth.forms import PasswordChangeForm
from client.mixins import ClientLoginRequiredMixin
from database.models import LaundryShop, Price, Transaction, Order, default_date

from LaundryBear.forms import LoginForm
from LaundryBear.views import LoginView, LogoutView

#Django uses class based views to connect with templates.
#Each class based view has their own methods.
#You can still add more methods if needed.
#Check ccbv.co.uk for more information

#Inherits Class Based View "LoginView"
class ClientLoginView(LoginView):
    template_name = "client/usersignin.html"
    form_class = LoginForm
    success_view_name = 'client:menu' #redirects to 'menu' after successful login


#Inherits Class Based View "LogoutView"
class ClientLogoutView(LogoutView):
    login_view_name = 'client:login' #redirects to 'login' after successful logout


#Inherits Class Based View "ListView"
class DashView(ClientLoginRequiredMixin, ListView): #Non-users cannot login with the help of ClientLoginRequiredMixin
    model = Transaction #aka self
    template_name = "client/dash.html"

    def get_context_data(self, **kwargs): #populates the dictionary context_data with the needed information for the template
        context = super(DashView, self).get_context_data(**kwargs)
        context['userprofile'] = self.request.user.userprofile
        context['transaction_list'] = self.get_transactions()
        context['fees'] = Site.objects.get_or_create(domain='laundrybear.pythonanywhere.com')[0].fees
        # context['fees'] = Site.objects.get_current().fees
        return context


    def get_transactions(self): #shows only the transactions made by the user
        queryset = super(DashView, self).get_queryset()
        queryset = queryset.filter(client=self.request.user.userprofile)
        return queryset

    def post(self, request, *args, **kwargs): #sets ratings
        the_post = request.POST
        transaction = Transaction.objects.get(pk=the_post['id'])
        transaction.paws = the_post['score']
        transaction.save()
        return redirect('client:menu') #redirects to 'menu' after rating a transaction from a laundry shop

#Inherits CBV "TemplateView"
class SignupView(TemplateView):
    template_name = "client/signup.html"

    def get_success_url(self): #redirects to 'menu' after user sign up
        return reverse('client:menu')

    def post(self, request):
        uf = UserForm(request.POST, prefix='user')
        upf = ProfileForm(request.POST, prefix='userprofile')
        # Note: in the ProfileForm do not include the user
        print 'post'
        if uf.is_valid() and upf.is_valid():  # check if both forms are valid
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()
            username = userprofile.user.username
            password = request.POST['user-password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('client:view-shops')
        else:
            print uf.errors
            print upf.errors
            return self.render_to_response({'userform': uf, 'userprofileform': upf, 'view': self})

    def get(self, request):
        uf = UserForm(prefix='user')
        upf = ProfileForm(prefix='userprofile')
        return render_to_response(SignupView.template_name,
                                  dict(userform=uf,
                                       userprofileform=upf),
                                  context_instance=RequestContext(request))

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.template_name, context=context, using=None, **response_kwargs)

#Inherits CBV "TemplateView"
class UserSettingsView(ClientLoginRequiredMixin, TemplateView):
    template_name = 'client/usersettings.html'

    def get_context_data(self, **kwargs):
        context = super(UserSettingsView, self).get_context_data(**kwargs)
        context['userprofile'] = self.request.user.userprofile
        context['userform'] = UserForm(data=self.request.POST or None, instance=self.request.user)
        context['userprofileform'] = ProfileForm(data=self.request.POST or None, instance=self.request.user.userprofile)
        context['usernameform'] = ChangeUsernameForm(data=self.request.POST or None, instance=self.request.user)
        context['passwordform'] = PasswordChangeForm(data=self.request.POST or None, user=self.request.user)
        return context

    def post(self,request,*args,**kwargs): #Saves data
        context = self.get_context_data(*args, **kwargs)
        userform = context['userform']
        userprofileform = context['userprofileform']
        usernameform = context['usernameform']
        passwordform = context['passwordform']

        #Check if forms are valid. If not, print errors
        if userform.is_valid():
            userform.save()
        else:
            print userform.errors


        if userprofileform.is_valid():
            userprofileform.save()
        else:
            print userprofileform.errors

        if (usernameform.is_valid()):
            usernameform.save()
        else:
            print usernameform.errors

        if passwordform.is_valid():
            passwordform.save()
            return redirect('client:menu')
        else:
            print passwordform.error_messages

        return self.render_to_response(context)

#Inherits CBV "ListView"
class ShopsListView(ClientLoginRequiredMixin, ListView):
    model = LaundryShop
    paginate_by = 10
    template_name="client/viewshops.html"
    context_object_name = 'shop_list'

    def get_context_data(self, **kwargs):
        context = super(ShopsListView, self).get_context_data(**kwargs)
        shops = context['shop_list']

        query_type = self.request.GET.get('query_type','')

        #Used for search with the use of filtering
        query = self.request.GET.get('browse', False)

        if query_type == 'name':
            shops = self.get_shops_by_name(query)
        elif query_type == 'city':
            shops = self.get_shops_by_city(query)
        elif query_type == 'province':
            shops = self.get_shops_by_province(query)
        elif query_type == 'barangay':
            shops = self.get_shops_by_barangay(query)
        else:
            shops = self.get_all_shops()

        context.update({'shop_list': shops})
        context['query_type'] = query_type
        context['fees'] = Site.objects.get_current().fees
        context['delivery_date'] = default_date().strftime('%Y-%m-%d')
        context['delivery_date_max'] = (default_date() + timedelta(days=7)).strftime('%Y-%m-%d')
        context['address_form'] = AddressForm(
            initial=model_to_dict(self.request.user.userprofile))
        return context

    #Get data needed by each search
    def get_shops_by_name(self, name_query):
        return LaundryShop.objects.filter(status=LaundryShop.ACTIVE,name__icontains=name_query)

    def get_shops_by_city(self, city_query):
        return LaundryShop.objects.filter(status=LaundryShop.ACTIVE,admin__city__icontains=city_query)

    def get_shops_by_province(self, province_query):
        return LaundryShop.objects.filter(status=LaundryShop.ACTIVE,admin__province__icontains=province_query)

    def get_shops_by_barangay(self, barangay_query):
        return LaundryShop.objects.filter(status=LaundryShop.ACTIVE,admin__barangay__icontains=barangay_query)

    def get_all_shops(self):
        return LaundryShop.objects.filter(status=LaundryShop.ACTIVE)

#Inherits CBV "DetailView"
class OrderView(ClientLoginRequiredMixin, DetailView):
    context_object_name = 'shop'
    model = LaundryShop
    template_name="client/shopselect.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        the_shop = context['shop']
        context['fees'] = Site.objects.get_or_create(domain='laundrybear.pythonanywhere.com')[0].fees
        context['service_list'] = Price.objects.filter(laundry_shop__name=the_shop)
        # context['fees'] = Site.objects.get_current().fees
        context['delivery_date'] = default_date().strftime('%Y-%m-%d')
        context['delivery_date_max'] = (default_date() + timedelta(days=7)).strftime('%Y-%m-%d')
        context['address_form'] = AddressForm(
            initial=model_to_dict(self.request.user.userprofile))
        return context

#Inherits CBV "DetailView"
class OrderSummaryView(ClientLoginRequiredMixin, DetailView):
    context_object_name = 'shop'
    template_name="client/summaryoforder.html"
    model=LaundryShop

    def get_context_data(self, **kwargs):
        context = super(OrderSummaryView, self).get_context_data(**kwargs)
        context['fees'] = Site.objects.get_or_create(domain='laundrybear.pythonanywhere.com')[0].fees
        context['delivery_date'] = default_date().strftime('%Y-%m-%d')
        context['delivery_date_max'] = (default_date() + timedelta(days=7)).strftime('%Y-%m-%d')
        context['address_form'] = AddressForm(
            initial=model_to_dict(self.request.user.userprofile))
        return context

    def post(self, request, *args, **kwargs):
        print request.POST['csrftoken']
        if request.is_ajax():
            services = request.POST['selectedServices']
            services = json.loads(services)
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = request.user.userprofile
                transaction.save()
            else:
                print transaction_form.errors
            for service in services:
                pricePk = service['pk']
                price = Price.objects.get(pk=pricePk)
                Order.objects.create(price=price, pieces=service['pieces'], transaction=transaction)
            print 'yes'
            # return HttpResponse(status=200)
            return HttpResponse(reverse('client:view-shops'))
        else:
            return HttpResponse(status=400)


#Inherits CBV "View"
class CreateTransactionView(ClientLoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateTransactionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=400)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            services = request.POST['selectedServices']
            services = json.loads(services)
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.client = request.user.userprofile
                transaction.save()
            else:
                print transaction_form.errors
            for service in services:
                pricePk = service['pk']
                price = Price.objects.get(pk=pricePk)
                Order.objects.create(price=price, pieces=service['pieces'], transaction=transaction)
            print 'yes'
            # return HttpResponse(status=200)
            return HttpResponse(reverse('client:view-shops'))
        else:
            return HttpResponse(status=400)
