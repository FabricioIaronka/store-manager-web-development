from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from .user_i_rep import UserIRep
from ...entities.user import User
from ...errors.user_error import UserEmailAlreadyExists
from ....infra.db.models.user_model import UserModel

class UserRep(UserIRep):
    def __init__(self, session: Session):
        self.session = session

    def _db_to_entity(self, user_db: UserModel) -> Optional[User]:
        return User(
                id=user_db.id,
                name=user_db.name,
                email=user_db.email,
                password_hash=user_db.password_hash,
                role=user_db.role,
                created_at=user_db.created_at,
                updated_at=user_db.updated_at
            )

    def create(self, user: User, h_password: str) -> User:
        """
            Join user with hashed password and updates database
        """
        try: 
            
            user_db = UserModel(
                name=user.name,
                email=user.email,
                password_hash=h_password,
                role=user.role
            )

            self.session.add(user_db)
            self.session.commit()
            self.session.refresh(user_db)

            return self._db_to_entity(user_db)
        
        except IntegrityError:
            self.session.rollback()
            raise UserEmailAlreadyExists
        
        except Exception as e:
            self.session.rollback()
            raise e
        
    def update(self, user_id: int, update_data: Dict[str, Any]) -> User | None:
        """
        Updates a user in the database.
        """
        user_db = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_db:
            return None

        for key, value in update_data.items():
            setattr(user_db, key, value)

        self.session.commit()
        self.session.refresh(user_db)

        return self._db_to_entity(user_db)
        
    def delete(self, user_id: int) -> bool:
        """
        Deletes a user from the database by their ID.
        Returns True if a user was deleted, False otherwise.
        """
        user_db = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_db:
            return False

        self.session.delete(user_db)
        self.session.commit()
        return True
    
    def get_by_id(self, user_id: int) -> User | None:
        user_db = self.session.query(UserModel).filter(UserModel.id == user_id).first()

        if not user_db:
            return None
        
        return self._db_to_entity(user_db)
    
    def get_by_email(self, email:str) -> User | None:
        user_db = self.session.query(UserModel).filter(UserModel.email == email).first()

        if not user_db:
            return None
        
        return self._db_to_entity(user_db)
    
    def get_all(self) -> List[User]:
        """"
            Get users from DB and groups in a list
        """
        try:
            users_db: List[UserModel] = self.session.query(UserModel).all()

            users = [
                self._db_to_entity(usr_db)
                for usr_db in users_db
            ]

            return users
        
        except OperationalError as e:
            raise e
        except Exception as e:
            raise e