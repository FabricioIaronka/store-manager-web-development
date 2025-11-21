from sqlalchemy import Column, Integer, Numeric, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from ....core.entities.payment_type import PaymentType


class SaleModel(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    payment_type = Column(
        SQLAlchemyEnum(
            PaymentType, 
            name="payment_type", 
            create_type=False,
            values_callable=lambda obj: [e.value for e in obj] 
        ), 
        nullable=False
    )

    total_value = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("SaleItemModel", back_populates="sale", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SaleModel(id={self.id}, total_value={self.total_value})>"


class SaleItemModel(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    sale = relationship("SaleModel", back_populates="items")

    def __repr__(self):
        return f"<SaleItemModel(sale_id={self.sale_id}, product_id={self.product_id}, quantity={self.quantity})>"