from abc import ABC, abstractmethod

from ..model import Document, User


class DocumentRepository(ABC):
    @abstractmethod
    def add_document(self, document: Document) -> Document:
        raise NotImplementedError("Implement add_document method")

    @abstractmethod
    def get_document(self, title: str, owner: User) -> Document:
        raise NotImplementedError("Implement get_document method")

    @abstractmethod
    def update_document(self, document: Document) -> Document:
        raise NotImplementedError("Implement update_document method")

    @abstractmethod
    def delete_document(self, title: str, owner: User) -> Document:
        raise NotImplementedError("Implement delete_document method")
