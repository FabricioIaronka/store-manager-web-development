from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from src.core.entities.user_role import UserRole


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    role: UserRole
    stores: List = field(default_factory=list)
    password_hash: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None