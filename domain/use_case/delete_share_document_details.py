from domain.repository import UserAccessDetailRepository


class DeleteShareDocumentDetails:
    def __init__(self, user_access_detail_repository: UserAccessDetailRepository):
        self.user_access_detail_repository = user_access_detail_repository

    def invoke(self, document_title: str, shared_user_username: str) -> bool:
        return self.user_access_detail_repository.delete_user_access_details(
            document_title, shared_user_username
        )
