import json

from django.http import JsonResponse
from django.views import View

from app.forms import DocumentForm
from di import DocumentUseCase, UserUseCase
from domain.model import Document


class DocumentView(View):
    def __init__(self):
        super().__init__()
        self.__document_use_case = DocumentUseCase()
        self.__user_use_case = UserUseCase()

    def get(self, request) -> JsonResponse:
        title = request.GET.get("documentTitle")
        document_owner_username = request.GET.get("documentOwnerUsername")

        if not (title and document_owner_username):
            documents = self.__document_use_case.get_all_documents().invoke()

            return JsonResponse(
                data={
                    "documentTitle": [document.title for document in documents],
                    "content": [document.content for document in documents],
                    "documentOwnerUsername": [
                        document.owner.username for document in documents
                    ],
                    "sharedUserUsernames": [
                        share_user.username
                        for document in documents
                        for share_user in document.shared_with
                    ],
                },
                status=200,
            )
        owner = self.__user_use_case.get_user().invoke(username=document_owner_username)
        document = self.__document_use_case.get_document_details().invoke(
            title=title, owner=owner
        )
        if document is None:
            return JsonResponse(data={"message": "Invalid payload"})

        return JsonResponse(
            data={
                "documentTitle": document.title,
                "content": document.content,
                "documentOwnerUsername": document.owner.username,
                "sharedUserUsernames": [
                    share_user.username for share_user in document.shared_with
                ],
                "message": "Document created successfully",
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

        document = self.__document_use_case.add_document().invoke(
            document=Document(
                form.cleaned_data.get("title"),
                form.cleaned_data.get("content"),
                form.cleaned_data.get("owner"),
                form.cleaned_data.get("shared_with"),
            )
        )

        return JsonResponse(
            data={
                "documentTitle": document.title,
                "content": document.content,
                "documentOwnerUsername": document.owner.username,
                "sharedUserUsernames": [
                    share_user.username for share_user in document.shared_with
                ],
                "message": "Document created successfully",
            },
            status=201,
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

        document = self.__document_use_case.update_document().invoke(
            document=Document(
                form.cleaned_data.get("title"),
                form.cleaned_data.get("content"),
                form.cleaned_data.get("owner"),
                form.cleaned_data.get("shared_with"),
            )
        )

        return JsonResponse(
            data={
                "documentTitle": document.title,
                "content": document.content,
                "documentOwnerUsername": document.owner.username,
                "sharedUserUsernames": [
                    share_user.username for share_user in document.shared_with
                ],
                "message": "Document updated successfully",
            }
        )

    def delete(self, request) -> JsonResponse:
        title = request.GET.get("documentTitle")
        document_owner_username = request.GET.get("documentOwnerUsername")

        owner = self.__user_use_case.get_user().invoke(username=document_owner_username)
        document = self.__document_use_case.get_document_details().invoke(
            title=title, owner=owner
        )
        if document is None:
            return JsonResponse(data={"message": "Invalid payload"})

        return JsonResponse(
            data={
                "documentTitle": document.title,
                "message": "Document deleted successfully",
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
