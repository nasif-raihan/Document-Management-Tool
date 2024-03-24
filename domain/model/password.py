import hashlib
import secrets


class Password:
    def __init__(self, password: str):
        self.password = password

    @property
    def salt(self) -> str:
        return secrets.token_hex(16)

    @property
    def hashed_password(self) -> str:
        salted_password = self.password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed_password

    def verify_password(self, new_password) -> bool:
        salted_password = new_password + self.salt
        new_hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return new_hashed_password == self.hashed_password
