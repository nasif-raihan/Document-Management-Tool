from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Document


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = "document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        user_documents = Document.objects.filter(owner=self.request.user)
        shared_documents = Document.objects.filter(shared_with=self.request.user)
        return (user_documents | shared_documents).distinct()
