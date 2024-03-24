from .password import Password


class User:
    def __init__(self, username: str, password: Password):
        self.username = username
        self.password = password
