from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import DocumentForm
from ..models import Document, UserAccessDetail


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "document_form.html"
    success_url = reverse_lazy("document_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        UserAccessDetail.objects.create(
            document=self.object,
            user=self.request.user,
            permission=UserAccessDetail.EDIT,
        )

        return response
