from dataclasses import dataclass

@dataclass
class SaleItem:
    sale_id: int
    product_id: int
    quantity: float
    unit_price: float