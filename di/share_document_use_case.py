from domain.use_case import (
    ShareDocument,
    GetShareDocumentDetails,
    UpdateShareDocumentDetails,
    DeleteShareDocumentDetails,
)
from .repository import Repository


class ShareDocumentUseCase:
    __instance = None

    def __init__(self):
        if self.__instance:
            raise RuntimeError("An instance of ShareDocumentUseCase is already running")

        self.__repository = Repository.get_instance()

    @classmethod
    def get_instance(cls) -> "ShareDocumentUseCase":
        if cls.__instance is None:
            cls.__instance = ShareDocumentUseCase()
        return cls.__instance

    def share_document(self) -> ShareDocument:
        return ShareDocument(
            user_access_detail_repository=self.__repository.user_access_detail_repository
        )

    def get_share_document_details(self) -> GetShareDocumentDetails:
        return GetShareDocumentDetails(
            user_access_detail_repository=self.__repository.user_access_detail_repository
        )

    def update_share_document_details(self) -> UpdateShareDocumentDetails:
        return UpdateShareDocumentDetails(
            user_access_detail_repository=self.__repository.user_access_detail_repository
        )

    def delete_share_document_details(self) -> DeleteShareDocumentDetails:
        return DeleteShareDocumentDetails(
            user_access_detail_repository=self.__repository.user_access_detail_repository
        )
