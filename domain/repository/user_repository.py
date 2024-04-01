from abc import ABC, abstractmethod

from ..model import User


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> User | None:
        raise NotImplementedError("Implement get_user method")
