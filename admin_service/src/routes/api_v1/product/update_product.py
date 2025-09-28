from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.routes.depends.external_api_services_depend import get_product_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.product.update_product import UpdateProduct
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/update/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_one_product(
    product: UpdateProductInput = Query(...),
    product_service: IProductService = Depends(get_product_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        update_product_usecase = UpdateProduct(product_service)
        output = await update_product_usecase.execute(user.credentials, product)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
