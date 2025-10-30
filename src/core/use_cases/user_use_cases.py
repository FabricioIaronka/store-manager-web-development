from typing import Any, Dict, List

from ...core.security import hash_password
from ..entities.user import User
from ..entities.user_role import UserRole
from ..errors.user_error import UserEmailAlreadyExists, UserNotFoundError
from ..interfaces.repository.user_rep import UserRep

class UserUseCase:
    def __init__(self, user_rep: UserRep):
        self.user_rep = user_rep

    def execute_create(self, name: str, email: str, password: str, role: UserRole) -> User:
        """
            Responsible to validate the user and call UserRep
        """

        if self.user_rep.get_by_email(email):
            raise UserEmailAlreadyExists(email)       

        h_password = hash_password(password)

        user = User(
            id=None,
            name= name,
            email= email,
            role= role
        )
        nw_user = self.user_rep.create(user, h_password)
        
        return nw_user
    
    def delete_user(self, user_id: int) -> None:
        """
        Validate deleting a user.
        """
        user_to_delete = self.user_rep.get_by_id(user_id)
        if not user_to_delete:
            raise UserNotFoundError()

        self.user_rep.delete(user_id)
        return
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> User:
        """
        Validate the update for a user.
        """
        user_to_update = self.user_rep.get_by_id(user_id)
        if not user_to_update:
            raise UserNotFoundError()

        new_email = user_data.get("email")
        if new_email:
            existing_user = self.user_rep.get_by_email(new_email)
            if existing_user and existing_user.id != user_id:
                raise UserEmailAlreadyExists(new_email)

        updated_user = self.user_rep.update(user_id, user_data)
        return updated_user
    
    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_rep.get_by_id(user_id)

        if not user:
            raise UserNotFoundError()
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.user_rep.get_by_email(email)

        if not user:
            raise UserNotFoundError()
        return user

    
    def get_users(self) -> List[User]:
        """"
            Returns all users
        """
        return self.user_rep.get_all()
