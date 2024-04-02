import logging

from app.models import Document as DBDocument, User as DBUser
from domain.model import Document
from domain.repository import DocumentRepository
from .db_user_repository import DBUserRepository

logger = logging.getLogger(__name__)


class DBDocumentRepository(DocumentRepository):
    def __init__(self):
        super().__init__()
        self._db_user_repository = DBUserRepository.get_instance()

    def add_document(self, document: Document) -> Document:
        old_document = self.get_document(
            title=document.title, owner_username=document.owner.username
        )
        if old_document is None:
            db_document = DBDocument(
                title=document.title,
                content=document.content,
                owner=DBUser.objects.get(username=document.owner.username),
            )
            db_document.save()

            # fmt: off
            for user in document.shared_with:
                shared_user = self._db_user_repository.get_user(username=user.username)
                if shared_user:
                    db_shared_user = self._db_user_repository.to_db_user(shared_user.username)
                    db_document.shared_with.add(db_shared_user)
                else:
                    db_document.shared_with.create(username=user.username)
            return self.to_document(db_document)
        return self.update_document(old_document)

    def get_document(self, title: str, owner_username: str) -> Document | None:
        try:
            db_document = DBDocument.objects.get(
                title=title, owner__username=owner_username
            )
        except DBDocument.DoesNotExist:
            return None
        return self.to_document(db_document)

    def get_all_documents(self) -> list[Document]:
        db_documents = DBDocument.objects.all()
        return [self.to_document(db_document) for db_document in db_documents]

    def update_document(self, document: Document) -> Document:
        try:
            # title and owner should not be updated
            db_document = DBDocument.objects.get(
                title=document.title, owner__username=document.owner.username
            )
        except DBDocument.DoesNotExist:
            raise RuntimeError("Invalid document information")

        db_document.title = document.title
        db_document.content = document.content
        db_document.owner = DBUser.objects.get(username=document.owner.username)

        # fmt: off
        for user in document.shared_with:
            shared_user = self._db_user_repository.get_user(username=user.username)
            if shared_user:
                db_shared_user = self._db_user_repository.to_db_user(shared_user.username)
                db_document.shared_with.add(db_shared_user)
            else:
                db_document.shared_with.create(username=user.username)
        # fmt: on
        return self.to_document(db_document)

    def delete_document(self, title: str, owner_username: str) -> bool:
        db_document = DBDocument.objects.get(
            title=title, owner__username=owner_username
        )
        if db_document is None:
            return False

        db_document.delete()
        return True

    @classmethod
    def to_document(cls, db_document: DBDocument) -> Document:
        return Document(
            title=db_document.title,
            content=db_document.content,
            owner=db_document.owner,
            shared_with=db_document.shared_with,
        )
