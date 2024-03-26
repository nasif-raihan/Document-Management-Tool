from app.models import UserAccessDetail as DBUserAccessDetail
from domain.model import UserAccessDetail
from domain.repository import UserAccessDetailRepository


class DBUserAccessDetailRepository(UserAccessDetailRepository):
    def create_user_access(
        self, user_access_detail: UserAccessDetail
    ) -> UserAccessDetail:
        if self.get_user_access_details(
            document_title=user_access_detail.document.title,
            shared_user_username=user_access_detail.user.username,
        ):
            return self.update_user_access_details(user_access_detail)

        db_user_access_detail = DBUserAccessDetail(
            document=user_access_detail.document,
            user=user_access_detail.user,
            permission_type=user_access_detail.permission_type,
        )
        db_user_access_detail.save()

        return self.to_user_access_detail(db_user_access_detail)

    def get_user_access_details(
        self, document_title: str, shared_user_username: str
    ) -> UserAccessDetail:
        try:
            db_user_access_detail = DBUserAccessDetail.objects.get(
                document__title=document_title, user__username=shared_user_username
            )
        except DBUserAccessDetail.DoesNotExist:
            raise RuntimeError("Invalid user access detail")
        return self.to_user_access_detail(db_user_access_detail)

    def update_user_access_details(
        self, user_access_detail: UserAccessDetail
    ) -> UserAccessDetail:
        try:
            db_user_access_detail = DBUserAccessDetail.objects.get(
                document__title=user_access_detail.document.title,
                user__username=user_access_detail.user.username,
            )
        except DBUserAccessDetail.DoesNotExist:
            raise RuntimeError("Invalid user access detail")

        db_user_access_detail.document = user_access_detail.document
        db_user_access_detail.user = user_access_detail.user
        db_user_access_detail.permission_type = user_access_detail.permission_type

        return self.to_user_access_detail(db_user_access_detail)

    def delete_user_access_details(
        self, document_title: str, shared_user_username: str
    ) -> UserAccessDetail:
        user_access_details = self.get_user_access_details(
            document_title, shared_user_username
        )
        db_user_access_detail = self.to_db_user_access_detail(user_access_details)
        db_user_access_detail.delete()
        return user_access_details

    @classmethod
    def to_db_user_access_detail(
        cls, user_access_detail: UserAccessDetail
    ) -> DBUserAccessDetail:
        return DBUserAccessDetail(
            document=user_access_detail.document,
            user=user_access_detail.user,
            permission_type=user_access_detail.permission_type,
        )

    @classmethod
    def to_user_access_detail(
        cls, db_user_access_detail: DBUserAccessDetail
    ) -> UserAccessDetail:
        return UserAccessDetail(
            document=db_user_access_detail.document,
            shared_user=db_user_access_detail.user,
            permission_type=db_user_access_detail.permission_type,
        )
