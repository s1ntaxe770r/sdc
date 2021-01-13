from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username",  "password1"]

def __init__(self, *args, **kwargs):
    super(UserCreationForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs= {
        'class' : 'fadeIn second',
        'placeholder' : 'username'
    }
    self.fields['password1'].widget.attr={
        'class' : 'fadeIn third',
        'placeholder' : 'password'
    }