from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from .sale_item import SaleItem
from .payment_type import PaymentType

@dataclass
class Sale:
    id: Optional[int]
    user_id: int
    client_id: int
    created_at: datetime
    payment_type: PaymentType
    total_value: float
    items: List[SaleItem] = field(default_factory=list)
    

