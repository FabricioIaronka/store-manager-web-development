from typing import List, Dict, Any
from ...core.entities.store import Store
from ...core.interfaces.repository.store_i_rep import StoreIRep
from ...core.errors.store_error import StoreNotFoundError, StoreCNPJAlreadyExistsError

class StoreUseCase:
    def __init__(self, store_rep: StoreIRep):
        self.store_rep = store_rep

    def create_store(self, name: str, cnpj: str, owner_id: int) -> Store:
        if self.store_rep.get_by_cnpj(cnpj):
            raise StoreCNPJAlreadyExistsError(cnpj)

        store = Store(
            id=None,
            name=name,
            cnpj=cnpj
        )
        return self.store_rep.create(store, owner_id)

    def get_all_stores(self) -> List[Store]:
        return self.store_rep.get_all()

    def get_store_by_id(self, store_id: int) -> Store:
        store = self.store_rep.get_by_id(store_id)
        if not store:
            raise StoreNotFoundError()
        return store

    def update_store(self, store_id: int, store_data: Dict[str, Any]) -> Store:
        current_store = self.store_rep.get_by_id(store_id)
        if not current_store:
            raise StoreNotFoundError()
        
        new_cnpj = store_data.get("cnpj")
        if new_cnpj and new_cnpj != current_store.cnpj:
            if self.store_rep.get_by_cnpj(new_cnpj):
                raise StoreCNPJAlreadyExistsError(new_cnpj)

        return self.store_rep.update(store_id, store_data)

    def delete_store(self, store_id: int) -> None:
        if not self.store_rep.get_by_id(store_id):
            raise StoreNotFoundError()
        self.store_rep.delete(store_id)