class ProductError(Exception):
    def __init__(self, msg: str):
        self.msg = f"PRODUCT ERROR -> {msg}"
        super().__init__(self.msg)

class ProductNotFoundError(ProductError):
    def __init__(self):
        super().__init__("Not found product with this attribute")

class ProductNameAlreadyExistsError(ProductError):
    def __init__(self, name: str):
        super().__init__(f"A product with this '{name}' already exists")