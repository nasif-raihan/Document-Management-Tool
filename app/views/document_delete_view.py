from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from ..models import Document


class DocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Document
    template_name = "document_confirm_delete.html"
    success_url = reverse_lazy("document_list")
    permission_required = "api.delete_document"

    def has_permission(self):
        document = self.get_object()
        return self.request.user == document.owner  # only owner has delete permission
