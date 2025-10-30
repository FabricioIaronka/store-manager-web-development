from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from .sale_item import SaleItem
from .payment_type import PaymentType

@dataclass
class Sale:
    id: Optional[int]
    client_id: int
    created_at: datetime
    payment_type: PaymentType
    items: List[SaleItem] = field(default_factory=list)

    @property
    def total_value(self) -> float:
        if not self.items:
            return 0.0
        total = sum(item.unit_price * item.quantity for item in self.items)
        return round(total, 2)

