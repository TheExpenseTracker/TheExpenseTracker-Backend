
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django import forms

from django.forms.widgets import PasswordInput, TextInput

# create a user(model form)
class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields= [ 'username', 'email', 'password1', 'password2']

# Authenticate a user(model form)
        
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fiels = '__all__'
        exclude = ['user']