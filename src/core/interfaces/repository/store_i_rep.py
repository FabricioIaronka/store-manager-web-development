from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ....core.entities.store import Store

class StoreIRep(ABC):
    @abstractmethod
    def create(self, store: Store, owner_id: int) -> Store:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, store_id: int) -> Optional[Store]:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_cnpj(self, cnpj: str) -> Optional[Store]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Store]:
        raise NotImplementedError

    @abstractmethod
    def update(self, store_id: int, store_data: Dict[str, Any]) -> Store:
        raise NotImplementedError

    @abstractmethod
    def delete(self, store_id: int) -> None:
        raise NotImplementedError