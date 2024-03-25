from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from ..forms import ShareDocumentForm
from ..models import Document, UserAccessDetail


class ShareDocumentView(LoginRequiredMixin, UpdateView):
    model = Document
    form_class = ShareDocumentForm
    template_name = "share_document.html"
    success_url = reverse_lazy("document_list")

    def get_object(self, queryset=None):
        document = super().get_object(queryset)

        try:
            UserAccessDetail.objects.get(document=document, user=self.request.user)
        except UserAccessDetail.DoesNotExist:
            raise PermissionDenied(
                "You do not have permission to access this document."
            )

        return document

    def form_valid(self, form):
        document = self.get_object()
        form.save_document_permissions(document)
        return super().form_valid(form)
