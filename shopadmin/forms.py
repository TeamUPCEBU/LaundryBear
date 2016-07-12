from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from database.models import ShopAdministrator

class ShopAdminForm(ModelForm): #Used in creating a shop admin profile
    class Meta:
        model = ShopAdministrator
        exclude = ['admin']
