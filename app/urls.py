from django.urls import path
from django.contrib.auth import views as auth_views
from app import forms, views

urlpatterns = [
    path("", views.base, name="base"),
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
]
