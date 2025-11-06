from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ....core.entities.client import Client

class ClientIRep(ABC):

    @abstractmethod
    def create(self, client: Client) -> Client:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, client_id: int) -> Optional[Client]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Client]:
        raise NotImplementedError

    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Optional[Client]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Client]:
        raise NotImplementedError

    @abstractmethod
    def update(self, client_id: int, client_data: Dict[str, Any]) -> Client:
        raise NotImplementedError

    @abstractmethod
    def delete(self, client_id: int) -> None:
        raise NotImplementedError