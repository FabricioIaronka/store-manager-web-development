from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.dependencies.auth_dependencies import get_session_with_rls
from ...core.interfaces.repository.store_rep import StoreRep
from ...core.use_cases.store_use_cases import StoreUseCase
from ...core.interfaces.repository.store_i_rep import StoreIRep

def get_store_repository(db: Session = Depends(get_session_with_rls)) -> StoreIRep:
    return StoreRep(session=db)

def get_store_use_cases(store_repository: StoreIRep = Depends(get_store_repository)) -> StoreUseCase:
    return StoreUseCase(store_rep=store_repository)