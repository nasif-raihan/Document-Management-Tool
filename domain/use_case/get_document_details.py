from domain.model import Document
from domain.repository import DocumentRepository


class GetDocumentDetails:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def invoke(self, title: str, owner_username: str) -> Document:
        return self.document_repository.get_document(title, owner_username)
