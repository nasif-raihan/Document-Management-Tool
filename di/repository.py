from data.repository import DBDocumentRepository, DBUserAccessDetailRepository
from domain.repository import DocumentRepository, UserAccessDetailRepository


class Repository:
    @property
    def document_repository(self) -> DocumentRepository:
        return DBDocumentRepository()

    @property
    def user_access_detail_repository(self) -> UserAccessDetailRepository:
        return DBUserAccessDetailRepository()
