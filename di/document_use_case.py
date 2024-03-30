from domain.use_case import (
    AddDocument,
    DeleteDocument,
    GetAllDocuments,
    GetDocumentDetails,
    UpdateDocument,
)
from .repository import Repository


class DocumentUseCase:
    __instance = None

    def __init__(self):
        if self.__instance:
            raise RuntimeError("An instance of DocumentUseCase is already running")

        self.__repository = Repository.get_instance()

    @classmethod
    def __get_instance(cls) -> "DocumentUseCase":
        if cls.__instance is None:
            cls.__instance = DocumentUseCase()
        return cls.__instance

    def add_document(self) -> AddDocument:
        return AddDocument(document_repository=self.__repository.document_repository)

    def delete_document(self) -> DeleteDocument:
        return DeleteDocument(document_repository=self.__repository.document_repository)

    def get_all_documents(self) -> GetAllDocuments:
        return GetAllDocuments(
            document_repository=self.__repository.document_repository
        )

    def get_document_details(self) -> GetDocumentDetails:
        return GetDocumentDetails(
            document_repository=self.__repository.document_repository
        )

    def update_document(self) -> UpdateDocument:
        return UpdateDocument(document_repository=self.__repository.document_repository)
