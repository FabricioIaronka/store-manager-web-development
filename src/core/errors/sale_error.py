class SaleError(Exception):
    def __init__(self, msg: str):
        self.msg = f"SALE ERROR -> {msg}"
        super().__init__(self.msg)

class SaleNotFoundError(SaleError):
    def __init__(self):
        super().__init__("Not found sale with this attribute")

class InsufficientStockError(SaleError):
    def __init__(self, product_name: str, requested: int, available: int):
        super().__init__(f"Insuficient quantity of '{product_name}'. Requested product: {requested}, Quantity avaliable: {available}.")