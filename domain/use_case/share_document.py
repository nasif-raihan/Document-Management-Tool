from domain.model import UserAccessDetail
from domain.repository import UserAccessDetailRepository


class ShareDocument:
    def __init__(self, user_access_detail_repository: UserAccessDetailRepository):
        self.user_access_detail_repository = user_access_detail_repository

    def invoke(self, user_access_detail: UserAccessDetail) -> UserAccessDetail:
        return self.user_access_detail_repository.create_user_access(user_access_detail)
