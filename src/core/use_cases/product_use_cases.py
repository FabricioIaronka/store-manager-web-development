from typing import List, Dict, Any
from ..entities.product import Product
from ..interfaces.repository.product_i_rep import ProductIRep
from ..errors.product_error import ProductNotFoundError, ProductNameAlreadyExistsError

class ProductUseCase:
    def __init__(self, product_rep: ProductIRep):
        self.product_rep = product_rep

    def create_product(self, store_id: int, name: str, description: str, price: float, qnt: int, category: str) -> Product:
        """ Responsible to validate new product and call ProductRep """

        if self.product_rep.get_by_name(name):
            raise ProductNameAlreadyExistsError(name)

        product = Product(
            id=None,
            store_id=store_id,
            name=name,
            description=description,
            price=price,
            qnt=qnt,
            category=category
        )
        return self.product_rep.create(product)

    def get_all_products(self) -> List[Product]:
        return self.product_rep.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        product = self.product_rep.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError()
        return product

    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Product:
        """ Responsible to validate updated product and call ProductRep """

        product_to_update = self.product_rep.get_by_id(product_id)
        if not product_to_update:
            raise ProductNotFoundError()
        
        new_name = product_data.get("name")
        if new_name:
            existing_product = self.product_rep.get_by_name(new_name)
            if existing_product and existing_product.id != product_id:
                raise ProductNameAlreadyExistsError(new_name)

        updated_product = self.product_rep.update(product_id, product_data)
        return updated_product

    def delete_product(self, product_id: int) -> None:
        """ Validate deleting product """
        product_to_delete = self.product_rep.get_by_id(product_id)
        if not product_to_delete:
            raise ProductNotFoundError()
        
        self.product_rep.delete(product_id)