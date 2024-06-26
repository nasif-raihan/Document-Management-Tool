import json
import logging

from django.http import JsonResponse
from django.views import View

from app.forms import DocumentForm
from di import DocumentUseCase, UserUseCase
from domain.model import Document

logger = logging.getLogger(__name__)


class DocumentView(View):
    def __init__(self):
        super().__init__()
        self.__document_use_case = DocumentUseCase()
        self.__user_use_case = UserUseCase()

    def get(self, request) -> JsonResponse:
        try:
            payload = json.loads(request.body)
            title = payload.get("documentTitle")
            owner_username = payload.get("documentOwnerUsername")
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "error": str(e)}
            )

        if title is None and owner_username is None:
            documents = self.__document_use_case.get_all_documents().invoke()
            documents_dict = []
            for document in documents:
                document_dict = {
                    "documentTitle": document.title,
                    "content": document.content,
                    "documentOwnerUsername": document.owner.username,
                    "sharedUserUsernames": [
                        user.username for user in document.shared_with.all()
                    ],
                }
                documents_dict.append(document_dict)

            return JsonResponse(
                data={
                    "documents": documents_dict,
                    "message": "Fetched all created documents.",
                },
                status=200,
            )

        owner = self.__user_use_case.get_user().invoke(username=owner_username)
        document = self.__document_use_case.get_document_details().invoke(
            title=title, owner_username=owner.username
        )
        if document is None:
            return JsonResponse(data={"message": "Invalid request payload"})
        print(f"{document.title=}")
        return JsonResponse(
            data={
                "documentTitle": document.title,
                "content": document.content,
                "documentOwnerUsername": document.owner.username,
                "sharedUserUsernames": [
                    share_user.username for share_user in document.shared_with.all()
                ],
            },
            status=200,
        )

    def post(self, request) -> JsonResponse:
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": str(e)}
            )

        form = self.__get_document_form(payload)

        if not form.is_valid():
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": form.errors}
            )

        title = form.cleaned_data.get("title")
        owner_username = form.cleaned_data.get("owner_username")
        shared_user_usernames = form.cleaned_data.get("shared_user_usernames")
        shared_users = []
        for shared_user_username in shared_user_usernames:
            shared_user = self.__user_use_case.get_user().invoke(
                username=shared_user_username
            )
            if shared_user:
                shared_users.append(shared_user)
        owner = self.__user_use_case.get_user().invoke(username=owner_username)
        document = self.__document_use_case.add_document().invoke(
            document=Document(
                title=title,
                content=form.cleaned_data.get("content"),
                owner=owner,
                shared_with=shared_users,
            )
        )

        return JsonResponse(
            data={
                "documentTitle": document.title,
                "content": document.content,
                "documentOwnerUsername": document.owner.username,
                "sharedUserUsernames": [
                    share_user.username for share_user in document.shared_with.all()
                ],
                "message": "Document created successfully",
            },
            status=201,
        )

    def put(self, request) -> JsonResponse:
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": str(e)}
            )

        form = self.__get_document_form(payload)

        if not form.is_valid():
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": form.errors}
            )

        title = form.cleaned_data.get("title")
        owner_username = form.cleaned_data.get("owner_username")
        shared_user_usernames = form.cleaned_data.get("shared_user_usernames")
        shared_users = []
        for shared_user_username in shared_user_usernames:
            shared_user = self.__user_use_case.get_user().invoke(
                username=shared_user_username
            )
            if shared_user:
                shared_users.append(shared_user)
        owner = self.__user_use_case.get_user().invoke(username=owner_username)
        document = self.__document_use_case.update_document().invoke(
            document=Document(
                title=title,
                content=form.cleaned_data.get("content"),
                owner=owner,
                shared_with=shared_users,
            )
        )

        return JsonResponse(
            data={
                "documentTitle": document.title,
                "content": document.content,
                "documentOwnerUsername": document.owner.username,
                "sharedUserUsernames": [
                    share_user.username for share_user in document.shared_with.all()
                ],
                "message": "Document updated successfully",
            },
            status=201,
        )

    def delete(self, request) -> JsonResponse:
        try:
            payload = json.loads(request.body)
            title = payload.get("documentTitle")
            owner_username = payload.get("documentOwnerUsername")
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "error": str(e)}
            )

        is_deleted = self.__document_use_case.delete_document().invoke(
            title, owner_username
        )
        if is_deleted:
            message = "Document deleted successfully"
        else:
            message = "No matching data is found for deletion"

        return JsonResponse(
            data={"isDeleted": is_deleted, "message": message},
            status=200,
        )

    @staticmethod
    def __get_document_form(data: dict) -> DocumentForm:
        return DocumentForm(
            data={
                "title": data.get("documentTitle"),
                "content": data.get("content"),
                "owner_username": data.get("documentOwnerUsername"),
                "shared_user_usernames": data.get("sharedUserUsernames"),
            }
        )
