import json

from django.http import JsonResponse
from django.views import View

from di import DocumentUseCase, ShareDocumentUseCase, UserUseCase
from domain.model import UserAccessDetail
from ..forms import ShareDocumentForm


class ShareDocumentView(View):
    def __init__(self):
        super().__init__()
        self.__document_use_case = DocumentUseCase()
        self.__user_use_case = UserUseCase()
        self.__share_document_use_case = ShareDocumentUseCase()

    def get(self, request) -> JsonResponse:
        document_title = request.GET.get("documentTitle")
        shared_user_username = request.GET.get("sharedUserUsername")

        user_access_detail = (
            self.__share_document_use_case.get_share_document_details().invoke(
                document_title, shared_user_username
            )
        )
        if user_access_detail is None:
            return JsonResponse(data={"message": "Invalid request payload"})

        return JsonResponse(
            data={
                "documentTitle": user_access_detail.document.title,
                "documentOwnerUsername": user_access_detail.document.owner,
                "permissionType": user_access_detail.permission_type,
                "sharedUserUsernames": shared_user_username,
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

        form = self.__get_share_document_form(data)
        if not form.is_valid():
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": form.errors}
            )

        document_title = form.cleaned_data.get("document_title")
        permission_type = form.cleaned_data.get("permission_type")
        document_owner_username = form.cleaned_data.get("document_owner_username")
        shared_user_usernames = form.cleaned_data.get("shared_user_usernames")
        user_access_detail_list = []
        # fmt: off
        document_owner = self.__user_use_case.get_user().invoke(username=document_owner_username)
        document = self.__document_use_case.get_document_details().invoke(title=document_title, owner=document_owner)
        for shared_user_username in shared_user_usernames:
            shared_user = self.__user_use_case.get_user().invoke(username=shared_user_username)
            user_access_detail = self.__share_document_use_case.share_document().invoke(
                UserAccessDetail(
                    shared_user=shared_user, document=document, permission_type=permission_type,
                )
            )
            user_access_detail_list.append(user_access_detail)
            # fmt: on

        return JsonResponse(
            data={
                "documentTitle": document_title,
                "documentOwnerUsername": document_owner,
                "permissionType": permission_type,
                "sharedUserUsernames": shared_user_usernames,
                "message": "Document shared successfully"
            },
            status=201
        )

    def put(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": str(e)}
            )

        form = self.__get_share_document_form(data)
        if not form.is_valid():
            return JsonResponse(
                data={"message": "Invalid request payload", "errors": form.errors}
            )

        document_title = form.cleaned_data.get("document_title")
        permission_type = form.cleaned_data.get("permission_type")
        document_owner_username = form.cleaned_data.get("document_owner_username")
        shared_user_usernames = form.cleaned_data.get("shared_user_usernames")
        user_access_detail_list = []
        # fmt: off
        document_owner = self.__user_use_case.get_user().invoke(username=document_owner_username)
        document = self.__document_use_case.get_document_details().invoke(title=document_title, owner=document_owner)
        for shared_user_username in shared_user_usernames:
            shared_user = self.__user_use_case.get_user().invoke(username=shared_user_username)
            user_access_detail = self.__share_document_use_case.update_share_document_details().invoke(
                UserAccessDetail(
                    shared_user=shared_user, document=document, permission_type=permission_type,
                )
            )
            user_access_detail_list.append(user_access_detail)
            # fmt: on

        return JsonResponse(
            data={
                "documentTitle": document_title,
                "documentOwnerUsername": document_owner,
                "permissionType": permission_type,
                "sharedUserUsernames": shared_user_usernames,
                "message": "Document access updated successfully"
            },
            status=200
        )

    def delete(self, request) -> JsonResponse:
        document_title = request.GET.get("documentTitle")
        shared_user_username = request.GET.get("sharedUserUsername")

        user_access_detail = (
            self.__share_document_use_case.delete_share_document_details().invoke(
                document_title, shared_user_username
            )
        )
        if user_access_detail is None:
            return JsonResponse(data={"message": "Invalid request payload"})

        return JsonResponse(
            data={
                "documentTitle": document_title,
                "documentOwnerUsername": user_access_detail.document.owner,
                "permissionType": user_access_detail.permission_type,
                "sharedUserUsernames": shared_user_username,
            },
            status=200,
        )

    @staticmethod
    def __get_share_document_form(data: dict) -> ShareDocumentForm:
        return ShareDocumentForm(
            data={
                "document_title": data.get("documentTitle"),
                "document_owner_username": data.get("documentOwnerUsername"),
                "permission_type": data.get("permissionType"),
                "shared_user_usernames": data.get("sharedUserUsernames"),
            }
        )
