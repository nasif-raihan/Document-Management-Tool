from domain.model import UserAccessDetail
from domain.repository import UserAccessDetailRepository


class GetShareDocumentDetails:
    def __init__(self, user_access_detail_repository: UserAccessDetailRepository):
        self.user_access_detail_repository = user_access_detail_repository

    def invoke(self, user_access_detail_id: int) -> UserAccessDetail:
        return self.user_access_detail_repository.get_user_access_detail(
            user_access_detail_id
        )
