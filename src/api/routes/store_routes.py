from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List

from src.core.use_cases.store_use_cases import StoreUseCase
from src.core.errors.store_error import StoreNotFoundError, StoreCNPJAlreadyExistsError
from src.core.entities.user import User
from src.api.dependencies.store_dependencies import get_store_use_cases
from src.api.dependencies.auth_dependencies import get_current_user
from src.api.schemas.store_schema import StoreCreate, StoreResponse, StoreUpdate

router = APIRouter(prefix="/stores", tags=["Stores"])

@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
def create_store(
    store_data: StoreCreate,
    store_use_cases: StoreUseCase = Depends(get_store_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        new_store = store_use_cases.create_store(
            name=store_data.name,
            cnpj=store_data.cnpj,
            owner_id=current_user.id
        )
        return new_store
    except StoreCNPJAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[StoreResponse])
def get_all_stores(
    store_use_cases: StoreUseCase = Depends(get_store_use_cases)
):
    try:
        return store_use_cases.get_all_stores()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{store_id}", response_model=StoreResponse)
def get_store_by_id(
    store_id: int,
    store_use_cases: StoreUseCase = Depends(get_store_use_cases)
):
    try:
        return store_use_cases.get_store_by_id(store_id)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: int,
    store_data: StoreUpdate,
    store_use_cases: StoreUseCase = Depends(get_store_use_cases)
):
    try:
        update_data = store_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado para atualizar")
            
        return store_use_cases.update_store(store_id, update_data)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StoreCNPJAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: int,
    store_use_cases: StoreUseCase = Depends(get_store_use_cases)
):
    try:
        store_use_cases.delete_store(store_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))