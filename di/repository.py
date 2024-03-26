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
    @property
    def document_repository(self) -> DocumentRepository:
        return DBDocumentRepository()

    @property
    def user_access_detail_repository(self) -> UserAccessDetailRepository:
        return DBUserAccessDetailRepository()

    @property
    def user_repository(self) -> UserRepository:
        return DBUserRepository()
