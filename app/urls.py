from django.contrib.auth import views as auth_views
from django.urls import path

from app import forms
from app import views as app_views

urlpatterns = [
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
    path('documents/', app_views.DocumentView.as_view(), name='document-list'),
    path('documents/create/', app_views.DocumentView.as_view(), name='document-create'),
    path('documents/<int:pk>/', app_views.DocumentView.as_view(), name='document-detail'),
    path('documents/<int:pk>/update/', app_views.DocumentView.as_view(), name='document-update'),
    path('documents/<int:pk>/delete/', app_views.DocumentView.as_view(), name='document-delete'),

    # Share Details URLS
    path('share-details/', app_views.ShareDocumentView.as_view(), name='share-details-list'),
    path('share-details/create/', app_views.ShareDocumentView.as_view(), name='share-details-create'),
    path('share-details/<int:pk>/', app_views.ShareDocumentView.as_view(), name='share-details-detail'),
    path('share-details/<int:pk>/update/', app_views.ShareDocumentView.as_view(), name='share-details-update'),
    path('share-details/<int:pk>/delete/', app_views.ShareDocumentView.as_view(), name='share-details-delete'),
    # fmt: on
]
