from fastapi import Depends
from sqlalchemy.orm import Session


from ...infra.db.database import get_db_session
from ...core.use_cases.user_use_cases import UserUseCase
from ...core.interfaces.repository.user_rep import UserRep

def get_user_repository(db: Session = Depends(get_db_session)) -> UserRep:
    return UserRep(session=db)

def get_user_use_cases(user_repository: UserRep = Depends(get_user_repository)) -> UserUseCase:
    """
        Returns UserUseCase with database session
    """
    return UserUseCase(user_rep=user_repository)