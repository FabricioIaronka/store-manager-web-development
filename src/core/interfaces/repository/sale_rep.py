from datetime import datetime
from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from ...entities.sale import Sale
from ...entities.sale_item import SaleItem
from ...interfaces.repository.sale_i_rep import SaleIRep
from ...errors.sale_error import InsufficientStockError
from ...errors.product_error import ProductNotFoundError

from ....infra.db.models.sale_model import SaleModel, SaleItemModel
from ....infra.db.models.product_model import ProductModel
from ...entities.payment_type import PaymentType

class SaleRep(SaleIRep):
    def __init__(self, session: Session):
        self.session = session

    def _db_to_entity(self, sale_db: SaleModel) -> Optional[Sale]:
        if not sale_db:
            return None
        
        sale_items_entities = [
            SaleItem(
                sale_id=item_db.sale_id,
                product_id=item_db.product_id,
                quantity=item_db.quantity,
                unit_price=float(item_db.unit_price)
            ) for item_db in sale_db.items
        ]
        
        return Sale(
            id=sale_db.id,
            store_id=sale_db.store_id,
            user_id=sale_db.user_id,
            client_id=sale_db.client_id,
            payment_type=PaymentType(sale_db.payment_type.value),
            total_value=float(sale_db.total_value),
            created_at=sale_db.created_at,
            items=sale_items_entities
        )

    def create(self, sale: Sale) -> Sale:
        """
        Cria a venda, os itens da venda e atualiza o estoque do produto.
        Tudo dentro de uma única transação.
        """
        try:
            sale_db = SaleModel(
                store_id=sale.store_id,
                user_id=sale.user_id,
                client_id=sale.client_id,
                payment_type=sale.payment_type, 
                total_value=sale.total_value,
                created_at=datetime.now() 
            )
            self.session.add(sale_db)
            self.session.flush() 

            for item_entity in sale.items:
                product_db = (
                    self.session.query(ProductModel)
                    .filter(ProductModel.id == item_entity.product_id)
                    .with_for_update() 
                    .first()
                )

                if not product_db:
                    raise ProductNotFoundError() 
                
                if product_db.quantity < item_entity.quantity:
                    raise InsufficientStockError(
                        product_name=product_db.name,
                        requested=item_entity.quantity,
                        available=product_db.quantity
                    )
                
                product_db.quantity -= item_entity.quantity
                
                sale_item_db = SaleItemModel(
                    sale_id=sale_db.id,
                    product_id=item_entity.product_id,
                    quantity=item_entity.quantity,
                    unit_price=item_entity.unit_price 
                )
                self.session.add(sale_item_db)

            self.session.commit()
            self.session.refresh(sale_db)
            
            return self._db_to_entity(sale_db)

        except (IntegrityError, InsufficientStockError, ProductNotFoundError) as e:
            self.session.rollback()
            raise e
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        sale_db = (
            self.session.query(SaleModel)
            .options(joinedload(SaleModel.items))
            .filter(SaleModel.id == sale_id)
            .first()
        )
        return self._db_to_entity(sale_db)

    def get_all(self) -> List[Sale]:
        sales_db = (
            self.session.query(SaleModel)
            .options(joinedload(SaleModel.items))
            .all()
        )
        return [self._db_to_entity(s) for s in sales_db]