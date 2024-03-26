from domain.use_case import GetUser
from .repository import Repository


class UserUseCase:
    def __init__(self):
        self.__repository = Repository()

    def get_user(self) -> GetUser:
        return GetUser(user_repository=self.__repository.user_repository)
