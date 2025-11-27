from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ClientModel(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=True)
    cpf = Column(String(11), unique=True, nullable=True)
    number = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=True)

    store = relationship("StoreModel", back_populates="clients")

    def __repr__(self):
        return f"<ClientModel(id={self.id}, name='{self.name}', email='{self.email}')>"