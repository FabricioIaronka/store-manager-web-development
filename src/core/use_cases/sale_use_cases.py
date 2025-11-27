from typing import List, Dict, Any, Optional
from datetime import datetime

from ..entities.sale import Sale
from ..entities.sale_item import SaleItem
from ..entities.payment_type import PaymentType

from ..interfaces.repository.sale_i_rep import SaleIRep
from ..interfaces.repository.product_i_rep import ProductIRep
from ..interfaces.repository.client_i_rep import ClientIRep
from ..interfaces.repository.user_i_rep import UserIRep

from ..errors.sale_error import SaleNotFoundError, InsufficientStockError
from ..errors.product_error import ProductNotFoundError
from ..errors.user_error import UserNotFoundError
from ..errors.client_error import ClientNotFoundError

class SaleUseCase:
    def __init__(
        self, 
        sale_rep: SaleIRep,
        product_rep: ProductIRep,
        client_rep: ClientIRep,
        user_rep: UserIRep
    ):
        self.sale_rep = sale_rep
        self.product_rep = product_rep
        self.client_rep = client_rep
        self.user_rep = user_rep

    def create_sale(
        self,
        store_id: int,
        user_id: int, 
        payment_type: PaymentType, 
        items: List[Dict[str, Any]], 
        client_id: Optional[int] = None
    ) -> Sale:
        
        if not self.user_rep.get_by_id(user_id):
            raise UserNotFoundError()

        if client_id and not self.client_rep.get_by_id(client_id):
            raise ClientNotFoundError()

        if not items:
            raise ValueError("Sale need at least have one item.")

        sale_items_entities = []
        total_value = 0.0

        for item_data in items:
            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity")

            product = self.product_rep.get_by_id(product_id)
            if not product:
                raise ProductNotFoundError() 
            
            if product.qnt < quantity:
                raise InsufficientStockError(
                    product_name=product.name,
                    requested=quantity,
                    available=product.qnt
                )
            
            unit_price = product.price
            total_value += (unit_price * quantity)

            sale_items_entities.append(
                SaleItem(
                    sale_id=0, 
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price
                )
            )

        sale_entity = Sale(
            id=None,
            store_id=store_id,
            user_id=user_id,
            client_id=client_id,
            payment_type=payment_type,
            total_value=round(total_value, 2),
            created_at=datetime.now(), 
            items=sale_items_entities
        )
        return self.sale_rep.create(sale_entity)

    def get_sale_by_id(self, sale_id: int) -> Sale:
        sale = self.sale_rep.get_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError()
        return sale

    def get_all_sales(self) -> List[Sale]:
        return self.sale_rep.get_all()