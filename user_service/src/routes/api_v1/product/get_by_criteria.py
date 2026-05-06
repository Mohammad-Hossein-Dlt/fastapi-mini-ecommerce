from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.product_filter_input import ProductFilterInput
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.routes.depends.internal_http_depend import product_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.product.get_by_criteria import GetProducts
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_criteria(
    criteria: ProductFilterInput = Query(...),
    product_service: IProductService = Depends(product_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_products_usecase = GetProducts(product_service)
        outputs_list = await get_products_usecase.execute(user.credentials, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
