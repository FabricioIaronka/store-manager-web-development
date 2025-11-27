from fastapi import Depends
from sqlalchemy.orm import Session

from .auth_dependencies import get_session_with_rls
from ...core.interfaces.repository.product_rep import ProductRep
from ...core.use_cases.product_use_cases import ProductUseCase
from ...core.interfaces.repository.product_i_rep import ProductIRep

def get_product_repository(db: Session = Depends(get_session_with_rls)) -> ProductIRep:
    return ProductRep(session=db)

def get_product_use_cases(product_repository: ProductIRep = Depends(get_product_repository)) -> ProductUseCase:
    return ProductUseCase(product_rep=product_repository)