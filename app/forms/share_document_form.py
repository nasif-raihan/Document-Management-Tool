from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from di.repository import Repository
from ..models import UserAccessDetail


class ShareDocumentForm(forms.ModelForm):
    document_title = forms.CharField(max_length=200)
    document_owner_username = forms.CharField(max_length=150)
    permission_type = forms.ChoiceField(choices=UserAccessDetail.PERMISSION_CHOICES)
    shared_user_usernames = forms.CharField(max_length=1500)  # maximum 10 usernames

    class Meta:
        model = UserAccessDetail
        fields = [
            "document_title",
            "document_owner_username",
            "permission_type",
            "shared_user_usernames",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["permission_type"].choices = UserAccessDetail.PERMISSION_CHOICES
        self.__repository = Repository.get_instance()

    def clean_shared_user_usernames(self):
        shared_user_usernames = self.cleaned_data.get("shared_user_usernames")
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
        document_title = self.cleaned_data.get("document_title")
        document_owner_username = self.cleaned_data.get("document_owner_username")
        shared_user_usernames = self.cleaned_data.get("shared_user_usernames")
        permission_type = self.cleaned_data.get("permission_type")

        document_owner = self.__repository.user_repository.get_user(
            username=document_owner_username
        )
        document = self.__repository.document_repository.get_document(
            title=document_title, owner_username=document_owner.username
        )
        user_access_detail_list = []
        for shared_person_username in shared_user_usernames:
            shared_user = self.__repository.user_repository.get_user(
                username=shared_person_username
            )
            user_access_detail, _ = UserAccessDetail.objects.update_or_create(
                document=document, user=shared_user, permission_type=permission_type
            )

        return user_access_detail_list
