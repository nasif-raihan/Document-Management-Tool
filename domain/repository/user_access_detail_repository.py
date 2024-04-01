from abc import ABC, abstractmethod

from ..model import UserAccessDetail


class UserAccessDetailRepository(ABC):
    @abstractmethod
    def create_user_access(
        self, user_access_detail: UserAccessDetail
    ) -> UserAccessDetail:
        raise NotImplementedError("Implement create_user_access method")

    @abstractmethod
    def get_user_access_details(
        self, document_title: str, shared_user_username: str
    ) -> UserAccessDetail | None:
        raise NotImplementedError("Implement get_user_access_detail method")

    @abstractmethod
    def update_user_access_details(
        self, user_access_detail: UserAccessDetail
    ) -> UserAccessDetail:
        raise NotImplementedError("Implement update_user_access_detail method")

    @abstractmethod
    def delete_user_access_details(
        self, document_title: str, shared_user_username: str
    ) -> bool:
        raise NotImplementedError("Implement delete_user_access_details method")
