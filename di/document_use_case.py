from domain.use_case import (
    AddDocument,
    DeleteDocument,
    GetAllDocuments,
    GetDocumentDetails,
    UpdateDocument,
)
from .repository import Repository


class DocumentUseCase:
    def __init__(self):
        self.repository = Repository()

    def add_document(self) -> AddDocument:
        return AddDocument(document_repository=self.repository.document_repository)

    def delete_document(self) -> DeleteDocument:
        return DeleteDocument(document_repository=self.repository.document_repository)

    def get_all_documents(self) -> GetAllDocuments:
        return GetAllDocuments(document_repository=self.repository.document_repository)

    def get_document_details(self) -> GetDocumentDetails:
        return GetDocumentDetails(
            document_repository=self.repository.document_repository
        )

    def update_document(self) -> UpdateDocument:
        return UpdateDocument(document_repository=self.repository.document_repository)
