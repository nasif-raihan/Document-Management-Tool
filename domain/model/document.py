from .user import User


class Document:
    def __init__(self, title: str, content: str, owner: User, shared_with: list[User]):
        self.title = title
        self.content = content
        self.owner = owner
        self.shared_with = shared_with
