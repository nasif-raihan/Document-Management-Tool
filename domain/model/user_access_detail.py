from .document import Document
from .permission_type import PermissionType
from .user import User


class UserAccessDetail:
    def __init__(
        self,
        user_access_detail_id: int,
        user: User,
        document: Document,
        permission_type: PermissionType,
    ):
        self.user_access_detail_id = user_access_detail_id
        self.user = user
        self.document = document
        self.permission_type = permission_type
