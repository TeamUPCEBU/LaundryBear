from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from database.models import UserProfile, Order, Transaction

#Forms are used for taking inputs
#Used for updates and creations
#Fiels are the information that can be modified/created.

class UserForm(UserCreationForm): #Used in creating a new user, or updating info of user
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'username', 'password1', 'password2']


class ProfileForm(ModelForm): #Used in creating a user profile, or updating info of user profile
    class Meta:
        model = UserProfile
        exclude = ['client'] #exclude client because it has a different specific form
