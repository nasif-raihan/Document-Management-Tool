from data.repository import (
    DBDocumentRepository,
    DBUserAccessDetailRepository,
    DBUserRepository,
)
from domain.repository import (
    DocumentRepository,
    UserAccessDetailRepository,
    UserRepository,
)


class Repository:
    __instance = None

    def __init__(self):
        if self.__instance:
            raise RuntimeError("An instance of Repository is already running")

    @classmethod
    def __get_instance(cls) -> "Repository":
        if cls.__instance is None:
            cls.__instance = Repository()
        return cls.__instance

    @property
    def document_repository(self) -> DocumentRepository:
        return DBDocumentRepository()

    @property
    def user_access_detail_repository(self) -> UserAccessDetailRepository:
        return DBUserAccessDetailRepository()

    @property
    def user_repository(self) -> UserRepository:
        return DBUserRepository()
