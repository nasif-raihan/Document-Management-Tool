from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DetailView

from ..models import Document


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "document_detail.html"
    context_object_name = "document"

    def get_queryset(self):
        user_documents = Document.objects.filter(owner=self.request.user)
        shared_documents = Document.objects.filter(shared_with=self.request.user)
        return (user_documents | shared_documents).distinct()

    def get_object(self, queryset=None):
        document = super().get_object(queryset)
        if (
            self.request.user == document.owner
            or self.request.user in document.shared_with.all()
        ):
            return document
        else:
            raise Http404("You do not have permission to view this document.")
