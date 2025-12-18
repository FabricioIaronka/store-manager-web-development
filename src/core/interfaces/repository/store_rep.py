from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ....core.entities.store import Store
from ....core.interfaces.repository.store_i_rep import StoreIRep
from ....core.errors.store_error import StoreCNPJAlreadyExistsError
from ....infra.db.models.store_model import StoreModel
from ....infra.db.models.user_model import UserModel

class StoreRep(StoreIRep):
    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, store_db: StoreModel) -> Optional[Store]:
        if not store_db:
            return None
        return Store(
            id=store_db.id,
            name=store_db.name,
            cnpj=store_db.cnpj,
            owner_id=store_db.owner_id,
            created_at=store_db.created_at
        )

    def create(self, store: Store, owner_id: int) -> Store:
        try:
            owner_db = self.session.query(UserModel).get(owner_id)
            if not owner_db:
                raise Exception("Owner User not found")

            store_db = StoreModel(
                name=store.name,
                cnpj=store.cnpj,
                owner_id=owner_id
            )

            store_db.users.append(owner_db)

            self.session.add(store_db)
            self.session.commit()
            self.session.refresh(store_db)

            return self._to_entity(store_db)

        except IntegrityError:
            self.session.rollback()
            raise StoreCNPJAlreadyExistsError(store.cnpj)
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, store_id: int) -> Optional[Store]:
        store_db = self.session.query(StoreModel).filter(StoreModel.id == store_id).first()
        return self._to_entity(store_db)

    def get_by_cnpj(self, cnpj: str) -> Optional[Store]:
        store_db = self.session.query(StoreModel).filter(StoreModel.cnpj == cnpj).first()
        return self._to_entity(store_db)

    def get_all(self) -> List[Store]:
        stores_db = self.session.query(StoreModel).all()
        return [self._to_entity(s) for s in stores_db]

    def update(self, store_id: int, store_data: Dict[str, Any]) -> Store:
        store_db = self.session.query(StoreModel).filter(StoreModel.id == store_id).first()
        if not store_db:
            return None

        update_data = {k: v for k, v in store_data.items() if v is not None}

        try:
            for key, value in update_data.items():
                setattr(store_db, key, value)
            
            self.session.commit()
            self.session.refresh(store_db)
            return self._to_entity(store_db)
        except IntegrityError:
            self.session.rollback()
            raise StoreCNPJAlreadyExistsError(update_data.get('cnpj'))
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, store_id: int) -> None:
        store_db = self.session.query(StoreModel).filter(StoreModel.id == store_id).first()
        if store_db:
            self.session.delete(store_db)
            self.session.commit()