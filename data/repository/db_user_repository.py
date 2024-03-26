from django.contrib.auth.models import User as DBUser

from domain.model import User
from domain.repository import UserRepository


class DBUserRepository(UserRepository):
    def get_user(self, username: str) -> User:
        try:
            db_user = DBUser.objects.get(username=username)
        except DBUser.DoesNotExist:
            raise RuntimeError("Username is not found")

        return self.to_user(db_user)

    @classmethod
    def to_user(cls, db_user: DBUser) -> User:
        return User(username=db_user.username, password=db_user.password)
