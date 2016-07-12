import json

from database.models import LaundryShop, Service, UserProfile, Transaction, Order, Fees

from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import (TemplateView)

from management import forms
from management.mixins import AdminLoginRequiredMixin

from LaundryBear.views import LoginView, LogoutView

#Django uses class based views to connect with templates.
#Each class based view has their own methods.
#You can still add more methods if needed.
#Check ccbv.co.uk for more information

class LaundryMenuView(AdminLoginRequiredMixin, TemplateView):
    template_name = 'management/shop/laundrybearmenu.html'


class AdminLoginView(LoginView):
    """ A view that only allows admins to login. """
    template_name = "management/account/login.html"
    form_class = forms.AdminLoginForm
    success_view_name = 'management:menu'


class AdminLogoutView(LogoutView):
    """ A view that logs out the user and redirects to the admin login. """
    login_view_name = 'management:login-admin'
