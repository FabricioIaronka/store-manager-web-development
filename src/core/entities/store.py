from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Store:
    id: Optional[int]
    name: str
    cnpj: str
    owner_id: Optional[int] = None
    created_at: Optional[datetime] = None