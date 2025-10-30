from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: Optional[int]
    name: str
    qnt: int
    description: str
    price: float
    category: Optional[str]

