from domain.model import UserAccessDetail
from domain.repository import UserAccessDetailRepository


class UpdateShareDocumentDetails:
    def __init__(self, user_access_detail_repository: UserAccessDetailRepository):
        self.user_access_detail_repository = user_access_detail_repository

    def invoke(self, user_access_detail: UserAccessDetail) -> UserAccessDetail:
        return self.user_access_detail_repository.update_user_access_detail(
            user_access_detail
        )
