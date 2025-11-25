# src/api/routes/product_routes.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List

from ...core.use_cases.product_use_cases import ProductUseCase
from ...core.errors.product_error import ProductNotFoundError, ProductNameAlreadyExistsError
from ...core.entities.user import User
from ...api.dependencies.auth_dependencies import get_current_user
from ..dependencies.product_dependencies import get_product_use_cases
from ..schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    product_use_cases: ProductUseCase = Depends(get_product_use_cases),
    current_user: User = Depends(get_current_user)
):
    """ Create new product """

    try:
        new_product = product_use_cases.create_product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            qnt=product_data.qnt,
            category=product_data.category
        )
        return new_product
    except ProductNameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    product_use_cases: ProductUseCase = Depends(get_product_use_cases),
    current_user: User = Depends(get_current_user)
):
    """ Get all products """

    try:
        products = product_use_cases.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    product_use_cases: ProductUseCase = Depends(get_product_use_cases),
    current_user: User = Depends(get_current_user)
):
    """ Get product by id """

    try:
        product = product_use_cases.get_product_by_id(product_id)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_use_cases: ProductUseCase = Depends(get_product_use_cases),
    current_user: User = Depends(get_current_user)
):
    """ Update product information by id """
    
    try:
        update_data = product_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização.")

        updated_product = product_use_cases.update_product(product_id, update_data)
        return updated_product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductNameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    product_use_cases: ProductUseCase = Depends(get_product_use_cases),
    current_user: User = Depends(get_current_user)
):
    """ Delete product from system """
    try:
        product_use_cases.delete_product(product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))