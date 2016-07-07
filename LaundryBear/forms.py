from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Username and/or password is incorrect.')
        return cleaned_data
