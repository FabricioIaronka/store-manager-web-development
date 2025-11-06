from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    surname: Optional[str] = Field(None, max_length=100)
    cpf: Optional[str] = Field(None, min_length=11, max_length=11) 
    number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    surname: Optional[str] = Field(None, max_length=100)
    cpf: Optional[str] = Field(None, min_length=11, max_length=11)
    number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None

class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True