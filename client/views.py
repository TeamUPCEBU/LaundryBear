import json

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import (ListView, TemplateView, View)

from client.forms import ProfileForm, UserForm

from client.mixins import ClientLoginRequiredMixin
from database.models import LaundryShop, Transaction, Order

from LaundryBear.forms import LoginForm
from LaundryBear.views import LoginView, LogoutView

#Inherits Class Based View "LoginView"
class ClientLoginView(LoginView):
    template_name = "client/usersignin.html"
    form_class = LoginForm
    success_view_name = 'client:menu' #redirects to 'menu' after successful login


#Inherits Class Based View "LogoutView"
class ClientLogoutView(LogoutView):
    login_view_name = 'client:login' #redirects to 'login' after successful logout


class DashView(ClientLoginRequiredMixin, TemplateView): #Non-users cannot login with the help of ClientLoginRequiredMixin
    template_name = "client/dash.html"



#Inherits CBV "TemplateView"
class SignupView(TemplateView):
    template_name = "client/signup.html"

    def get_success_url(self): #redirects to 'menu' after user sign up
        return reverse('client:menu')

    def post(self, request):
        uf = UserForm(request.POST, prefix='user')
        upf = ProfileForm(request.POST, prefix='userprofile')
        # Note: in the ProfileForm do not include the user
        if uf.is_valid() and upf.is_valid():  # check if both forms are valid
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.client = user
            userprofile.save()
            username = userprofile.client.username
            password = request.POST['user-password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('client:menu')
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
