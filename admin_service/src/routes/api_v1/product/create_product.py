from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.product.create_product_input import CreateProductInput
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.routes.depends.external_api_services_depend import get_product_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.product.create_product import CreateProduct
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/create",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_product(
    product: CreateProductInput = Query(...),
    product_service: IProductService = Depends(get_product_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        create_product_usecase = CreateProduct(product_service)
        output = await create_product_usecase.execute(user.credentials, product)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
 