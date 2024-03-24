from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": "True"}))
    password = forms.CharField(
        strip=False,
        label=gettext_lazy("Password"),
        widget=forms.PasswordInput(attrs={"auto-complete": "current-password"}),
    )
