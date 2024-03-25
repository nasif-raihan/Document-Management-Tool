from domain.use_case import (
    ShareDocument,
    GetShareDocumentDetails,
    UpdateShareDocumentDetails,
)
from .repository import Repository


class ShareDocumentUseCase:
    def __init__(self):
        self.repository = Repository()

    def share_document(self) -> ShareDocument:
        return ShareDocument(
            user_access_detail_repository=self.repository.user_access_detail_repository
        )

    def get_share_document_details(self) -> GetShareDocumentDetails:
        return GetShareDocumentDetails(
            user_access_detail_repository=self.repository.user_access_detail_repository
        )

    def update_share_document_details(self) -> UpdateShareDocumentDetails:
        return UpdateShareDocumentDetails(
            user_access_detail_repository=self.repository.user_access_detail_repository
        )
