class StoreError(Exception):
    def __init__(self, msg: str):
        self.msg = f"STORE ERROR -> {msg}"
        super().__init__(self.msg)

class StoreNotFoundError(StoreError):
    def __init__(self):
        super().__init__("Store not found.")

class StoreCNPJAlreadyExistsError(StoreError):
    def __init__(self, cnpj: str):
        super().__init__(f"Already exists a store with this CNPJ '{cnpj}'.")