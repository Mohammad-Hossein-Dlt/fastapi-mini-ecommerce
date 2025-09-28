from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.product.get_product import GetProduct
from src.repo.interface.Iproduct_repo import IProductRepo
from src.routes.depends.product_repo_depend import get_product_repo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.category_repo_depend import get_category_repo
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_one_product(
    product_id: str = Query(...),
    product_repo: IProductRepo = Depends(get_product_repo),
    category_repo: ICategoryRepo = Depends(get_category_repo),
    user: UserModel = Depends(user_auth_depend),
): 
    try:
        get_product_usecase = GetProduct(product_repo, category_repo)
        output = await get_product_usecase.execute(product_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
