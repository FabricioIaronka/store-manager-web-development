from abc import ABC, abstractmethod
from typing import Optional, List

from ....core.entities.user import User


class UserIRep(ABC):

    @abstractmethod
    def create(user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(id: int) -> Optional[User]:
        raise NotImplementedError
    
    @abstractmethod
    def get_all() -> List[User]:
        raise NotImplementedError
    
    @abstractmethod
    def delete(user: User) -> Optional[User]:
        raise NotImplementedError