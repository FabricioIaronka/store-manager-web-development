from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from ..database import Base
from ....core.entities.user_role import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(SQLAlchemyEnum(UserRole, name="user_role", create_type=False), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<UserModel(id={self.id}, name='{self.name}', role='{self.role.value}')>"