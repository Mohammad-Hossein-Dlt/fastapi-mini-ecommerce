from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.product.delete_product import DeleteProduct
from src.repo.interface.Iproduct_repo import IProductRepo
from src.routes.depends.product_repo_depend import get_product_repo
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete/one",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_one_product(
    product_id: str = Query(...),
    product_repo: IProductRepo = Depends(get_product_repo),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_product_usecase = DeleteProduct(product_repo)
        output = await delete_product_usecase.execute(product_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
