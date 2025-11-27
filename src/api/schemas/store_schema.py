from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StoreBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    cnpj: str = Field(..., min_length=14, max_length=18)

class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    cnpj: Optional[str] = Field(None, min_length=14, max_length=18)

class StoreResponse(StoreBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True