from django import forms
from database.models import *
from LaundryBear.forms import LoginForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdminLoginForm(LoginForm):
    def clean(self):
        cleaned_data = super(AdminLoginForm, self).clean()
        user = cleaned_data.get('user')

        if not user.is_staff:
            raise forms.ValidationError('You have no power here.')


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'username', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['client']
