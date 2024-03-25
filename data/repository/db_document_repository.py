from app.models import Document as DBDocument
from domain.model import User, Document
from domain.repository import DocumentRepository


class DBDocumentRepository(DocumentRepository):
    def add_document(self, document: Document) -> Document:
        if self.get_document(title=document.title, owner=document.owner):
            return self.update_document(document)

        db_document = DBDocument(
            title=document.title,
            content=document.content,
            owner=document.owner,
            shared_with=document.shared_with,
        )
        db_document.save()
        return self.to_document(db_document)

    def get_document(self, title: str, owner: User) -> Document:
        try:
            db_document = DBDocument.objects.get(title=title, owner=owner)
        except DBDocument.DoesNotExist:
            raise RuntimeError("Invalid document information")
        return self.to_document(db_document)

    def get_all_documents(self) -> list[Document]:
        db_documents = DBDocument.objects.all()
        return [self.to_document(db_document) for db_document in db_documents]

    def update_document(self, document: Document) -> Document:
        try:
            db_document = DBDocument.objects.get(
                title=document.title, owner=document.owner
            )
        except DBDocument.DoesNotExist:
            raise RuntimeError("Invalid document information")

        db_document.title = document.title
        db_document.content = document.content
        db_document.owner = document.owner
        db_document.shared_with = document.shared_with
        return self.to_document(db_document)

    def delete_document(self, title: str, owner: User) -> Document:
        document = self.get_document(title, owner)
        db_document = self.to_db_document(document)
        db_document.delete()
        return document

    @classmethod
    def to_db_document(cls, document: Document) -> DBDocument:
        return DBDocument(
            title=document.title,
            content=document.content,
            owner=document.owner,
            shared_with=document.shared_with,
        )

    @classmethod
    def to_document(cls, db_document: DBDocument) -> Document:
        return Document(
            title=db_document.title,
            content=db_document.content,
            owner=db_document.owner,
            shared_with=db_document.shared_with,
        )
