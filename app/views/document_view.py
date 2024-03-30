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
        title = request.GET.get("documentTitle")
        owner_username = request.GET.get("documentOwnerUsername")

        # fmt: off
        logger.debug(f"documentTitle={request.GET.get('documentTitle')}")
        logger.debug(f"{title=}")
        logger.debug(f"documentOwnerUsername={request.GET.get('documentOwnerUsername')}")
        logger.debug(f"{owner_username=}")
        # fmt: on

        if title is None and owner_username is None:
            documents = self.__document_use_case.get_all_documents().invoke()
            for document in documents:
                print(f"{document=}")
            return JsonResponse(
                data={
                    "documentTitle": [document.title for document in documents],
                    "content": [document.content for document in documents],
                    "documentOwnerUsername": [
                        document.owner.username for document in documents
                    ],
                    "sharedUserUsernames": [
                        document.shared_with for document in documents
                    ],
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
                    share_user.username for share_user in document.shared_with
                ],
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
                    share_user.username for share_user in document.shared_with
                ],
                "message": "Document updated successfully",
            },
            status=201,
        )

    def delete(self, request) -> JsonResponse:
        title = request.GET.get("documentTitle")
        owner_username = request.GET.get("documentOwnerUsername")

        owner = self.__user_use_case.get_user().invoke(username=owner_username)
        document = self.__document_use_case.get_document_details().invoke(
            title=title, owner_username=owner.username
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
                "title": data.get("documentTitle"),
                "content": data.get("content"),
                "owner_username": data.get("documentOwnerUsername"),
                "shared_user_usernames": data.get("sharedUserUsernames"),
            }
        )
