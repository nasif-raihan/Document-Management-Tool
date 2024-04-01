from domain.model import UserAccessDetail
from domain.repository import UserAccessDetailRepository


class GetShareDocumentDetails:
    def __init__(self, user_access_detail_repository: UserAccessDetailRepository):
        self.user_access_detail_repository = user_access_detail_repository

    def invoke(
        self, document_title: str, shared_user_username: str
    ) -> UserAccessDetail | None:
        return self.user_access_detail_repository.get_user_access_details(
            document_title, shared_user_username
        )
