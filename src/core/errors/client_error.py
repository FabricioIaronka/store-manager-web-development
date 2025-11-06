class ClientError(Exception):
    def __init__(self, msg: str):
        self.msg = f"CLIENT ERROR -> {msg}"
        super().__init__(self.msg)

class ClientNotFoundError(ClientError):
    def __init__(self):
        super().__init__("Client not found with this atributte.")

class ClientEmailAlreadyExistsError(ClientError):
    def __init__(self, email: str):
        super().__init__(f"Client with this '{email}' already exists.")

class ClientCPFAlreadyExistsError(ClientError):
    def __init__(self, cpf: str):
        super().__init__(f"Client with this CPF'{cpf}' already exists.")