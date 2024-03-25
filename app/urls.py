from django.contrib.auth import views as auth_views
from django.urls import path

from app import forms, views

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
    path("", views.DocumentListView.as_view(), name="document_list"),
    path(
        "document/<int:pk>/", views.DocumentDetailView.as_view(), name="document_detail"
    ),
    path(
        "document/create/", views.DocumentCreateView.as_view(), name="document_create"
    ),
    path(
        "document/<int:pk>/update/",
        views.DocumentUpdateView.as_view(),
        name="document_update",
    ),
    path(
        "document/<int:pk>/delete/",
        views.DocumentDeleteView.as_view(),
        name="document_delete",
    ),
    path(
        "document/<int:pk>/share/",
        views.ShareDocumentView.as_view(),
        name="share_document",
    ),
]
