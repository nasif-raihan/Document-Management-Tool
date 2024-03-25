from app.models import UserAccessDetail as DBUserAccessDetail
from domain.model import UserAccessDetail
from domain.repository import UserAccessDetailRepository


class DBUserAccessDetailRepository(UserAccessDetailRepository):
    def create_user_access(
        self, user_access_detail: UserAccessDetail
    ) -> UserAccessDetail:
        if self.get_user_access_detail(
            user_access_detail_id=user_access_detail.user_access_detail_id
        ):
            return self.update_user_access_detail(user_access_detail)

        db_user_access_detail = DBUserAccessDetail(
            document=user_access_detail.document,
            user=user_access_detail.user,
            permission_type=user_access_detail.permission_type,
        )
        db_user_access_detail.save()

        return self.to_user_access_detail(db_user_access_detail)

    def get_user_access_detail(self, user_access_detail_id: int) -> UserAccessDetail:
        try:
            db_user_access_detail = DBUserAccessDetail.objects.get(
                id=user_access_detail_id
            )
        except DBUserAccessDetail.DoesNotExist:
            raise RuntimeError("Invalid user access detail")
        return self.to_user_access_detail(db_user_access_detail)

    def update_user_access_detail(
        self, user_access_detail: UserAccessDetail
    ) -> UserAccessDetail:
        try:
            db_user_access_detail = DBUserAccessDetail.objects.get(
                id=user_access_detail.user_access_detail_id
            )
        except DBUserAccessDetail.DoesNotExist:
            raise RuntimeError("Invalid user access detail")

        db_user_access_detail.document = user_access_detail.document
        db_user_access_detail.user = user_access_detail.user
        db_user_access_detail.permission_type = user_access_detail.permission_type

        return self.to_user_access_detail(db_user_access_detail)

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
            user_access_detail_id=db_user_access_detail.id,
            document=db_user_access_detail.document,
            user=db_user_access_detail.user,
            permission_type=db_user_access_detail.permission_type,
        )
