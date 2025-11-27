from dataclasses import dataclass
from typing import Optional

@dataclass
class Client:
    id: Optional[int]
    store_id: int
    name: str
    surname: str
    cpf: str
    number: str
    email: str