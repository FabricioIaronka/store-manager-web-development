from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ....core.entities.client import Client
from ....core.interfaces.repository.client_i_rep import ClientIRep
from ....core.errors.client_error import ClientEmailAlreadyExistsError, ClientCPFAlreadyExistsError
from ....infra.db.models.client_model import ClientModel

class ClientRep(ClientIRep):

    def __init__(self, session: Session):
        self.session = session

    def _db_to_entity(self, client_db: ClientModel) -> Client:
        """Converts DB model into Entity"""
        if not client_db:
            return None
        return Client(
            id=client_db.id,
            name=client_db.name,
            surname=client_db.surname,
            cpf=client_db.cpf,
            number=client_db.number,
            email=client_db.email
        )

    def create(self, client: Client) -> Client:
        try:
            client_db = ClientModel(
                name=client.name,
                surname=client.surname,
                cpf=client.cpf,
                number=client.number,
                email=client.email
            )
            self.session.add(client_db)
            self.session.commit()
            self.session.refresh(client_db)
            return self._db_to_entity(client_db)
            
        except IntegrityError as e:
            self.session.rollback()
            
            if "clients_email_key" in str(e):
                raise ClientEmailAlreadyExistsError(client.email)
            if "clients_cpf_key" in str(e):
                raise ClientCPFAlreadyExistsError(client.cpf)
            raise e
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, client_id: int) -> Optional[Client]:
        client_db = self.session.query(ClientModel).filter(ClientModel.id == client_id).first()
        return self._db_to_entity(client_db)

    def get_by_email(self, email: str) -> Optional[Client]:
        client_db = self.session.query(ClientModel).filter(ClientModel.email == email).first()
        return self._db_to_entity(client_db)

    def get_by_cpf(self, cpf: str) -> Optional[Client]:
        client_db = self.session.query(ClientModel).filter(ClientModel.cpf == cpf).first()
        return self._db_to_entity(client_db)

    def get_all(self) -> List[Client]:
        clients_db = self.session.query(ClientModel).all()
        return [self._db_to_entity(c) for c in clients_db]

    def update(self, client_id: int, client_data: Dict[str, Any]) -> Client:
        client_db = self.session.query(ClientModel).filter(ClientModel.id == client_id).first()
        if not client_db:
            return None

        update_data = {k: v for k, v in client_data.items() if v is not None}

        try:
            for key, value in update_data.items():
                setattr(client_db, key, value)
            
            self.session.commit()
            self.session.refresh(client_db)
            return self._db_to_entity(client_db)
            
        except IntegrityError as e:
            self.session.rollback()
            if "clients_email_key" in str(e):
                raise ClientEmailAlreadyExistsError(update_data["email"])
            if "clients_cpf_key" in str(e):
                raise ClientCPFAlreadyExistsError(update_data["cpf"])
            raise e
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, client_id: int) -> None:
        client_db = self.session.query(ClientModel).filter(ClientModel.id == client_id).first()
        if client_db:
            self.session.delete(client_db)
            self.session.commit()