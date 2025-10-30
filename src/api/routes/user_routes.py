from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List

from ...core.use_cases.user_use_cases import UserUseCase
from ...core.errors.user_error import UserNotFoundError, UserEmailAlreadyExists
from ..dependencies.user_dependencies import get_user_use_cases
from ..schemas.user_schema import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    user_use_cases: UserUseCase = Depends(get_user_use_cases)
):
    """
        Create system user
    """
    try:
        
        new_user = user_use_cases.execute_create(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role
        )
        return new_user
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_use_cases: UserUseCase = Depends(get_user_use_cases)
):
    """
        Updates a user's information.
    """

    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided."
        )
    try:
        updated_user = user_use_cases.update_user(user_id, update_data)
        return updated_user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserEmailAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_use_cases: UserUseCase = Depends(get_user_use_cases)
):
    """
    Deletes a user from the system by their ID.
    """
    try:
        user_use_cases.delete_user(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int, 
    user_use_cases: UserUseCase = Depends(get_user_use_cases)
):
    """Search user by id"""
    try:
        user = user_use_cases.get_user_by_id(user_id)
        return user
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/email/{user_email}", response_model=UserResponse)
def get_user_by_email(
    user_email: str,
    user_use_cases: UserUseCase = Depends(get_user_use_cases)
):
    """Search user by email"""
    try:
        user = user_use_cases.get_user_by_email(user_email)
        return user
    
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(user_use_cases: UserUseCase = Depends(get_user_use_cases)):
    """
        Returns all registered users
    """
    try:
        return user_use_cases.get_users()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )