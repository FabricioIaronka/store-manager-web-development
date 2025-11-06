from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ....core.entities.product import Product

class ProductIRep(ABC):

    @abstractmethod
    def create(self, product: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def update(self, product_id: int, product_data: Dict[str, Any]) -> Product:
        raise NotImplementedError

    @abstractmethod
    def delete(self, product_id: int) -> None:
        raise NotImplementedError