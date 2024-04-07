from typing import Protocol
from ...models.user import User

class UserRepositoryProtocol(Protocol):
    def get_user(self, user_id: int) -> User:
        pass

    def create_user(self, user: User) -> User:
        pass

    def update_user(self, user_id: User, user: User) -> User:
        pass

    def delete_user(self, user_id: User) -> User:
        pass