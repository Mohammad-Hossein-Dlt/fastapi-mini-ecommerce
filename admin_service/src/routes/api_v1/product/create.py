from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.product.create_product_input import CreateProductInput
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.routes.depends.internal_http_depend import product_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.product.create import CreateProduct
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateProductInput = Query(...),
    product_service: IProductService = Depends(product_service_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        create_product_usecase = CreateProduct(product_service)
        output = await create_product_usecase.execute(user.credentials, entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
 