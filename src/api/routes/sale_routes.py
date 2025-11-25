from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...core.use_cases.sale_use_cases import SaleUseCase
from ...api.dependencies.sale_dependencies import get_sale_use_cases
from ...api.schemas.sale_schema import SaleCreate, SaleResponse

from ...core.errors.sale_error import SaleNotFoundError, InsufficientStockError
from ...core.errors.product_error import ProductNotFoundError
from ...core.errors.user_error import UserNotFoundError
from ...core.errors.client_error import ClientNotFoundError
from ...core.entities.user import User
from ...api.dependencies.auth_dependencies import get_current_user

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_data: SaleCreate,
    sale_use_cases: SaleUseCase = Depends(get_sale_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        items_list_dict = [item.model_dump() for item in sale_data.items]
        
        new_sale = sale_use_cases.create_sale(
            user_id=sale_data.user_id,
            payment_type=sale_data.payment_type,
            client_id=sale_data.client_id,
            items=items_list_dict
        )
        
        return new_sale
        
    except (ProductNotFoundError, UserNotFoundError, ClientNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except InsufficientStockError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[SaleResponse])
def get_all_sales(
    sale_use_cases: SaleUseCase = Depends(get_sale_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        sales = sale_use_cases.get_all_sales()
        return sales
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale_by_id(
    sale_id: int,
    sale_use_cases: SaleUseCase = Depends(get_sale_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        sale = sale_use_cases.get_sale_by_id(sale_id)
        return sale
    except SaleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_44_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))