from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ....core.entities.product import Product
from ....core.interfaces.repository.product_i_rep import ProductIRep
from ....core.errors.product_error import ProductNameAlreadyExistsError
from ....infra.db.models.product_model import ProductModel

class ProductRep(ProductIRep):
    def __init__(self, session: Session):
        self.session = session

    def _db_to_entity(self, product_db: ProductModel) -> Product:
        """Converts DB model into Entity"""
        if not product_db:
            return None
        return Product(
                id=product_db.id,
                store_id=product_db.store_id,
                name=product_db.name,
                description=product_db.description,
                price=float(product_db.price),
                qnt=product_db.quantity,
                category=product_db.category
            )


    def create(self, product: Product) -> Product:
        """ Create the ProductModel and commit on db """
        try:
            product_db = ProductModel(
                name=product.name,
                store_id=product.store_id,
                description=product.description,
                price=product.price,
                quantity=product.qnt, 
                category=product.category
            )
            self.session.add(product_db)
            self.session.commit()
            self.session.refresh(product_db)
            
            return self._db_to_entity(product_db)
        
        except IntegrityError:
            self.session.rollback()
            raise ProductNameAlreadyExistsError(name=product.name)
        except Exception as e:
            print(e)
            self.session.rollback()
            raise e

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """ Return the product by id """
        
        product_db = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()

        if not product_db:
            return None
        
        return self._db_to_entity(product_db)

    def get_by_name(self, name: str) -> Optional[Product]:
        """ Return the product by name """

        product_db = self.session.query(ProductModel).filter(ProductModel.name == name).first()
        
        if not product_db:
            return None
        
        return self._db_to_entity(product_db)

    def get_all(self) -> List[Product]:
        """ Returns all products """

        products_db = self.session.query(ProductModel).all()
        
        return [
            self._db_to_entity(p)
            for p in products_db
        ]

    def update(self, product_id: int, product_data: Dict[str, Any]) -> Product:
        """ Join the old product with the new and commit on db """
        
        product_db = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        
        if not product_db:
            return None 
        
        update_data = {
            "name": product_data.get("name"),
            "description": product_data.get("description"),
            "price": product_data.get("price"),
            "quantity": product_data.get("qnt"),
            "category": product_data.get("category")
        }
        
        update_data = {k: v for k, v in update_data.items() if v is not None}

        try:
            for key, value in update_data.items():
                setattr(product_db, key, value)
            
            self.session.commit()
            self.session.refresh(product_db)
            
            return self._db_to_entity(product_db)
        
        except IntegrityError:
            self.session.rollback()
            raise ProductNameAlreadyExistsError(name=update_data["name"])
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, product_id: int) -> None:
        """ Delete the product by id """
        
        product_db = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product_db:
            self.session.delete(product_db)
            self.session.commit()