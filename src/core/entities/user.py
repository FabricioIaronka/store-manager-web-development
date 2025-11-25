from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.core.entities.user_role import UserRole


@dataclass
class User:
    id: Optional[int]
    name: str
    password_hash: str
    email: str
    role: UserRole

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None