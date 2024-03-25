from domain.model import Document
from domain.repository import DocumentRepository


class GetAllDocuments:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def invoke(self) -> list[Document]:
        return self.document_repository.get_all_documents()
