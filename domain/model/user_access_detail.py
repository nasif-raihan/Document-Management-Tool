from .document import Document
from .permission_type import PermissionType
from .user import User


class UserAccessDetail:
    def __init__(
        self,
        shared_user: User,
        document: Document,
        permission_type: PermissionType,
    ):
        self.user = shared_user
        self.document = document
        self.permission_type = permission_type
