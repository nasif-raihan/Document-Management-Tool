from django.contrib.auth.models import User as DBUser

from domain.model import User, Password
from domain.repository import UserRepository


class DBUserRepository(UserRepository):
    __instance = None

    def __init__(self):
        if self.__instance:
            raise RuntimeError("An instance of DBUserRepository is already running")

    @classmethod
    def get_instance(cls) -> "DBUserRepository":
        if cls.__instance is None:
            cls.__instance = DBUserRepository()
        return cls.__instance

    def get_user(self, username: str) -> DBUser | None:
        try:
            db_user = DBUser.objects.get(username=username)
        except DBUser.DoesNotExist:
            return None
        return self.to_user(db_user)

    @classmethod
    def to_user(cls, db_user: DBUser) -> User:
        return User(username=db_user.username, password=Password(db_user.password))

    @classmethod
    def to_db_user(cls, username: str) -> DBUser:
        return DBUser.objects.get(username=username)
