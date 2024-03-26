from ..model import User
from ..repository import UserRepository


class GetUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def invoke(self, username: str) -> User:
        return self.user_repository.get_user(username)
