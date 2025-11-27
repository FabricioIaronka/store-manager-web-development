from fastapi import Depends
from sqlalchemy.orm import Session

from ..dependencies.user_dependencies import get_user_repository
from ..dependencies.product_dependencies import get_product_repository
from ..dependencies.client_dependencies import get_client_repository

from .auth_dependencies import get_session_with_rls
from ...core.interfaces.repository.sale_rep import SaleRep
from ...core.interfaces.repository.sale_i_rep import SaleIRep

from ...core.use_cases.sale_use_cases import SaleUseCase

from ...core.interfaces.repository.user_i_rep import UserIRep
from ...core.interfaces.repository.product_i_rep import ProductIRep
from ...core.interfaces.repository.client_i_rep import ClientIRep


def get_sale_repository(db: Session = Depends(get_session_with_rls)) -> SaleIRep:
    return SaleRep(session=db)

def get_sale_use_cases(
    sale_rep: SaleIRep = Depends(get_sale_repository),
    product_rep: ProductIRep = Depends(get_product_repository),
    client_rep: ClientIRep = Depends(get_client_repository),
    user_rep: UserIRep = Depends(get_user_repository)
) -> SaleUseCase:
    return SaleUseCase(
        sale_rep=sale_rep,
        product_rep=product_rep,
        client_rep=client_rep,
        user_rep=user_rep
    )