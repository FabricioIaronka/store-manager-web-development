from typing import List, Dict, Any, Optional
from ..entities.client import Client
from ..interfaces.repository.client_i_rep import ClientIRep
from ..errors.client_error import ClientNotFoundError, ClientEmailAlreadyExistsError, ClientCPFAlreadyExistsError

class ClientUseCase:    
    def __init__(self, client_rep: ClientIRep):
        self.client_rep = client_rep

    def create_client(self, store_id: int, name: str, surname: Optional[str], cpf: Optional[str], number: Optional[str], email: Optional[str]) -> Client:
        
        if email and self.client_rep.get_by_email(email):
            raise ClientEmailAlreadyExistsError(email)
        
        if cpf and self.client_rep.get_by_cpf(cpf):
            raise ClientCPFAlreadyExistsError(cpf)

        client = Client(
            id=None,
            store_id=store_id,
            name=name,
            surname=surname,
            cpf=cpf,
            number=number,
            email=email
        )
        return self.client_rep.create(client)

    def get_all_clients(self) -> List[Client]:
        return self.client_rep.get_all()

    def get_client_by_id(self, client_id: int) -> Client:
        client = self.client_rep.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError()
        return client

    def get_client_by_cpf(self, client_cpf: str) -> Client:
        client = self.client_rep.get_by_cpf(client_cpf)
        if not client:
            raise ClientNotFoundError()
        return client

    def get_client_by_email(self, client_email: str) -> Client:
        client = self.client_rep.get_by_email(client_email)
        if not client:
            raise ClientNotFoundError()
        return client

    def update_client(self, client_id: int, client_data: Dict[str, Any]) -> Client:
        client_to_update = self.client_rep.get_by_id(client_id)
        if not client_to_update:
            raise ClientNotFoundError()
        
        new_email = client_data.get("email")
        if new_email:
            existing_client = self.client_rep.get_by_email(new_email)
            if existing_client and existing_client.id != client_id:
                raise ClientEmailAlreadyExistsError(new_email)

        new_cpf = client_data.get("cpf")
        if new_cpf:
            existing_client = self.client_rep.get_by_cpf(new_cpf)
            if existing_client and existing_client.id != client_id:
                raise ClientCPFAlreadyExistsError(new_cpf)

        updated_client = self.client_rep.update(client_id, client_data)
        return updated_client

    def delete_client(self, client_id: int) -> None:
        client_to_delete = self.client_rep.get_by_id(client_id)
        if not client_to_delete:
            raise ClientNotFoundError()
        
        self.client_rep.delete(client_id)