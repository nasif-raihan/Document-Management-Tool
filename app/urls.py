from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app import forms
from app import views as app_views

urlpatterns = [
    path("registration/", app_views.RegistrationView.as_view(), name="registration"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="app/login.html", authentication_form=forms.LoginForm
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    # fmt: off
    # Document URLS
    path('documents/', csrf_exempt(app_views.DocumentView.as_view()), name='document'),

    # Share Details URLS
    path('share-details/', csrf_exempt(app_views.ShareDocumentView.as_view()), name='share-details'),
    # fmt: off
]
