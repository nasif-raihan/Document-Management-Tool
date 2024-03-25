from domain.model import Document
from domain.repository import DocumentRepository


class AddDocument:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def invoke(self, document: Document) -> Document:
        return self.document_repository.add_document(document)
