from fastapi import Depends
from sqlalchemy.orm import Session

from .auth_dependencies import get_session_with_rls
from ...core.use_cases.client_use_cases import ClientUseCase
from ...core.interfaces.repository.client_rep import ClientRep
from ...core.interfaces.repository.client_i_rep import ClientIRep

def get_client_repository(db: Session = Depends(get_session_with_rls)) -> ClientIRep:
    return ClientRep(session=db)

def get_client_use_cases(client_repository: ClientIRep = Depends(get_client_repository)) -> ClientUseCase:
    return ClientUseCase(client_rep=client_repository)