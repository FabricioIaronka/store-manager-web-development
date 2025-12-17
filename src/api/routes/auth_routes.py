from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas.auth_schema import LoginResponse
from ..schemas.user_schema import UserResponse
from ..dependencies.auth_dependencies import get_current_user
from ...infra.db.database import get_db_session
from ...core.interfaces.repository.user_rep import UserRep
from ...core.entities.user import User
from ...core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session)
):
    """
    Verify email and psswd. Returns JWT token
    """
    user_rep = UserRep(db)
    user = user_rep.get_user_for_auth(form_data.username) 

    if not user or not verify_password(form_data.password, user.password_hash): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Return the logged user
    """
    return current_user