import json

from django.http import JsonResponse
from django.views import View

from app.forms import DocumentForm
from di import DocumentUseCase
from domain.model import Document


class DocumentView(View):
    def __init__(self):
        super().__init__()
        self.__use_case = DocumentUseCase()

    def get(self, request) -> JsonResponse:
        title = request.GET.get("documentTitle")
        document_owner_username = request.GET.get("documentOwnerUsername")

        owner = self.__use_case.
        document = self.__use_case.get_document_details().invoke(
            title=title, owner=owner
        )

        if document is None:
            return JsonResponse(data={"message": "Invalid payload"})

        return JsonResponse(
            data={
                "title": document.title,
                "content": document.content,
                "owner": document.owner,
                "shared_with": document.shared_with,
            },
            status=200,
        )

    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": str(e)}
            )

        form = self.__get_document_form(data)

        if not form.is_valid():
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": form.errors}
            )

        document = self.__use_case.add_document().invoke(
            document=Document(
                form.cleaned_data.get("title"),
                form.cleaned_data.get("content"),
                form.cleaned_data.get("owner"),
                form.cleaned_data.get("sharedWith"),
            )
        )

        return JsonResponse(
            data={
                "title": document.title,
                "content": document.content,
                "owner": document.owner,
                "shared_with": document.shared_with,
            }
        )

    def put(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": str(e)}
            )

        form = self.__get_document_form(data)

        if not form.is_valid():
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": form.errors}
            )

        document = self.__use_case.update_document().invoke(
            document=Document(
                form.cleaned_data.get("title"),
                form.cleaned_data.get("content"),
                form.cleaned_data.get("owner"),
                form.cleaned_data.get("sharedWith"),
            )
        )

        return JsonResponse(
            data={
                "title": document.title,
                "content": document.content,
                "owner": document.owner,
                "shared_with": document.shared_with,
            }
        )

    def delete(self, request) -> JsonResponse:
        title = request.GET.get("title")
        owner = request.GET.get("owner")

        document = self.__use_case.delete_document().invoke(title=title, owner=owner)

        if document is None:
            return JsonResponse(data={"message": "Invalid payload"})

        return JsonResponse(
            data={
                "title": document.title,
                "content": document.content,
                "owner": document.owner,
                "shared_with": document.shared_with,
            },
            status=200,
        )

    @staticmethod
    def __get_document_form(data: dict) -> DocumentForm:
        return DocumentForm(
            data={
                "title": data.get("title"),
                "content": data.get("content"),
                "owner": data.get("owner"),
                "shared_with": data.get("sharedWith"),
            }
        )
