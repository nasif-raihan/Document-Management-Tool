from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError

from ..models import Document, UserAccessDetail


class ShareDocumentForm(forms.ModelForm):
    shared_with = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Document
        fields = ["shared_with"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for user in self.fields["shared_with"].queryset:
            field_name = f"permission_{user.id}"
            self.fields[field_name] = forms.ChoiceField(
                choices=UserAccessDetail.PERMISSION_CHOICES,
                label=f"Permission for {user.username}",
            )

    def save_document_permissions(self, document):
        for user in self.fields["shared_with"].queryset:
            field_name = f"permission_{user.id}"
            permission_type = self.cleaned_data.get(field_name)
            if permission_type:
                existing_permission = UserAccessDetail.objects.filter(
                    document=document, user=user
                ).first()
                if existing_permission:
                    existing_permission.permission = permission_type
                    existing_permission.save()
                else:
                    try:
                        UserAccessDetail.objects.create(
                            document=document, user=user, permission=permission_type
                        )
                    except IntegrityError:
                        raise RuntimeError("Unique constraint is violated")
