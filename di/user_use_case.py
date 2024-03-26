from domain.use_case import GetUser
from .repository import Repository


class UserUseCase:
    __instance = None

    def __init__(self):
        if self.__instance:
            raise RuntimeError("An instance of UserUseCase is already running")

        self.__repository = Repository()

    @classmethod
    def __get_instance(cls) -> "UserUseCase":
        if cls.__instance is None:
            cls.__instance = UserUseCase()
        return cls.__instance

    def get_user(self) -> GetUser:
        return GetUser(user_repository=self.__repository.user_repository)
