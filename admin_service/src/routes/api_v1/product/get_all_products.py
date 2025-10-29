from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.routes.depends.internal_http_depend import product_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.product.get_all_products import GetAllProducts
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_products(
    product_filter: ProductFilterInput = Query(...),
    product_service: IProductService = Depends(product_service_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_all_user_products_usecase = GetAllProducts(product_service)
        outputs_list = await get_all_user_products_usecase.execute(user.credentials, product_filter)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
