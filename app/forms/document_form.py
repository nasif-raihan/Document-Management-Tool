import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from di import Repository
from ..models import Document


class DocumentForm(forms.ModelForm):
    owner_username = forms.CharField(max_length=150)
    shared_user_usernames = forms.CharField(max_length=1500)  # maximum 10 usernames

    class Meta:
        model = Document
        fields = (
            "title",
            "content",
            "owner_username",
            "shared_user_usernames",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__repository = Repository.get_instance()

    def clean_shared_user_usernames(self):
        shared_user_usernames_str = self.cleaned_data.get("shared_user_usernames")
        shared_user_usernames = re.sub(r"['\[\]]", "", shared_user_usernames_str)
        usernames_list = [
            username.strip() for username in shared_user_usernames.split(",")
        ]
        for username in usernames_list:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                raise ValidationError(
                    f"User with username '{username}' does not exist."
                )
        return usernames_list

    def save(self, commit=True):
        title = self.cleaned_data.get("document_title")
        content = self.cleaned_data.get("content")
        owner_username = self.cleaned_data.get("owner_username")
        shared_user_usernames = self.cleaned_data.get("shared_user_usernames")

        document_owner = self.__repository.user_repository.get_user(
            username=owner_username
        )
        shared_users = []
        for shared_user_username in shared_user_usernames:
            shared_user = self.__repository.user_repository.get_user(
                username=shared_user_username
            )
            shared_users.append(shared_user)

        document, _ = Document.objects.update_or_create(
            title=title,
            content=content,
            owner=document_owner,
            shared_with=shared_users,
        )

        return document
