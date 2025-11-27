import os
from dotenv import load_dotenv
from fastapi import  Header, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import text

from ...infra.db.database import get_db_session, get_tenant_session
from ...core.entities.user import User
from ...core.interfaces.repository.user_rep import UserRep

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid crendencials or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    db.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))

    user_rep = UserRep(db)
    user = user_rep.get_by_id(int(user_id))
    
    if user is None:
        raise credentials_exception
        
    return user

def get_session_with_rls(current_user: User = Depends(get_current_user)):
    yield from get_tenant_session(current_user.id)


def get_active_store_id(
    x_store_id: int = Header(..., alias="x-store-id"),
    current_user: User = Depends(get_current_user)
) -> int:
    """
    Get Store ID and validate if the user have access to this store
    """
    
    if not current_user.stores:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User don't have asssociated stores."
        )

    allowed_store_ids = [store.id for store in current_user.stores]

    if x_store_id not in allowed_store_ids:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Access denied to {x_store_id}. You don't have permission."
        )

    return x_store_id