from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


user_store_association = Table(
    'user_stores',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('store_id', Integer, ForeignKey('stores.id', ondelete="CASCADE"), primary_key=True)
)

class StoreModel(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
    users = relationship(
        "UserModel", 
        secondary=user_store_association, 
        back_populates="stores"
    )

    sales = relationship(
        "SaleModel", 
        back_populates="store",
        cascade="all, delete-orphan" 
    )

    products = relationship(
        "ProductModel", 
        back_populates="store",
        cascade="all, delete-orphan"
    )

    clients = relationship(
        "ClientModel", 
        back_populates="store",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<StoreModel(id={self.id}, name='{self.name}')>"