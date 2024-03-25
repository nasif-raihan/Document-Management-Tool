from domain.model import Document, User
from domain.repository import DocumentRepository


class DeleteDocument:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def invoke(self, title: str, owner: User) -> Document:
        return self.document_repository.delete_document(title, owner)
