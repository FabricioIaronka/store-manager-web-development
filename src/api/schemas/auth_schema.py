from pydantic import BaseModel
from src.api.schemas.user_schema import UserResponse

class LoginResponse(BaseModel):
    access_token: str
    token_type: str