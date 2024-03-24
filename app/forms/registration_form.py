from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password")
    password2 = forms.CharField(label="Confirm Password")
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
