from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas.auth_schema import LoginResponse
from ..schemas.user_schema import UserResponse
from ..dependencies.auth_dependencies import get_current_user
from ...infra.db.database import get_db_session
from ...core.interfaces.repository.user_rep import UserRep
from ...core.entities.user import User
from ...core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login_for_access_token(
    response: Response,
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

    cookie_expire_seconds = ACCESS_TOKEN_EXPIRE_MINUTES * 60

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=cookie_expire_seconds,  
        expires=cookie_expire_seconds,
        samesite="none",   
        secure=True     
    )
    
    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    """
    Clears the HttpOnly cookie
    """
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Return the logged user
    """
    return current_user