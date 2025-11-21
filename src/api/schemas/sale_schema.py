from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ...core.entities.payment_type import PaymentType


class SaleItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemResponse(SaleItemBase):
    unit_price: float

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    payment_type: PaymentType
    client_id: Optional[int] = None

class SaleCreate(SaleBase):
    user_id: int 
    items: List[SaleItemCreate] = Field(..., min_items=1)

class SaleResponse(SaleBase):
    id: int
    user_id: int
    total_value: float
    created_at: datetime
    items: List[SaleItemResponse]

    class Config:
        from_attributes = True
        use_enum_values = True