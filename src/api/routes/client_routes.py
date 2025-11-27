from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List

from ...core.use_cases.client_use_cases import ClientUseCase
from ...core.errors.client_error import ClientNotFoundError, ClientEmailAlreadyExistsError, ClientCPFAlreadyExistsError
from ...core.entities.user import User
from ..dependencies.client_dependencies import get_client_use_cases
from ..dependencies.auth_dependencies import get_active_store_id
from ..schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    client_use_cases: ClientUseCase = Depends(get_client_use_cases),
    store_id: int = Depends(get_active_store_id)
):
    try:
        new_client = client_use_cases.create_client(
            store_id=store_id,
            name=client_data.name,
            surname=client_data.surname,
            cpf=client_data.cpf,
            number=client_data.number,
            email=client_data.email
        )
        return new_client
    except (ClientEmailAlreadyExistsError, ClientCPFAlreadyExistsError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ClientResponse])
def get_all_clients(
    client_use_cases: ClientUseCase = Depends(get_client_use_cases)
):
    try:
        clients = client_use_cases.get_all_clients()
        return clients
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(
    client_id: int,
    client_use_cases: ClientUseCase = Depends(get_client_use_cases)
):
    try:
        client = client_use_cases.get_client_by_id(client_id)
        return client
    except ClientNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/cpf/{client_cpf}", response_model=ClientResponse)
def get_client_by_cpf(
    client_cpf: str,
    client_use_cases: ClientUseCase = Depends(get_client_use_cases)
):
    try:
        client = client_use_cases.get_client_by_cpf(client_cpf)
        return client
    except ClientNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/email/{client_email}", response_model=ClientResponse)
def get_client_by_email(
    client_email: str,
    client_use_cases: ClientUseCase = Depends(get_client_use_cases)
):
    try:
        client = client_use_cases.get_client_by_email(client_email)
        return client
    except ClientNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    client_use_cases: ClientUseCase = Depends(get_client_use_cases)
):
    try:
        update_data = client_data.model_dump(exclude_unset=True) 
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização.")

        updated_client = client_use_cases.update_client(client_id, update_data)
        return updated_client
    except ClientNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ClientEmailAlreadyExistsError, ClientCPFAlreadyExistsError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    client_use_cases: ClientUseCase = Depends(get_client_use_cases)
):
    try:
        client_use_cases.delete_client(client_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ClientNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))