from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from ..forms import DocumentForm
from ..models import Document, UserAccessDetail


class DocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = "document_form.html"
    success_url = reverse_lazy("document_list")
    permission_required = "api.change_document"

    def get_queryset(self):
        user_documents = Document.objects.filter(owner=self.request.user)
        shared_documents = Document.objects.filter(shared_with=self.request.user)
        access_detail_documents = UserAccessDetail.objects.filter(
            user=self.request.user
        )
        access_associated_documents = Document.objects.filter(
            useraccessdetail__in=access_detail_documents
        )

        # Combine the query sets and remove duplicates
        queryset = (
            user_documents | shared_documents | access_associated_documents
        ).distinct()

        return queryset

    def has_permission(self):
        document = self.get_object()
        try:
            user_permission = UserAccessDetail.objects.get(
                document=document, user=self.request.user
            )
            return user_permission.permission == UserAccessDetail.EDIT
        except UserAccessDetail.DoesNotExist:
            return False
