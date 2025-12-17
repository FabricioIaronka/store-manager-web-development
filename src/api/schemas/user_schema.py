from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from ...core.entities.user_role import UserRole
from ..schemas.store_schema import StoreResponse


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    stores: List[StoreResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
