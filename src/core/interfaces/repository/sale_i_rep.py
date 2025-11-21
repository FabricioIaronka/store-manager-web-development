from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities.sale import Sale

class SaleIRep(ABC):

    @abstractmethod
    def create(self, sale: Sale) -> Sale:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Sale]:
        raise NotImplementedError