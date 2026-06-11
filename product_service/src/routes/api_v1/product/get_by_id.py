from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.product.get_by_id import GetProduct
from src.repo.interface.Iproduct_repo import IProductRepo
from src.routes.depends.repo_depend import product_repo_depend
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_id(
    product_id: str = Query(...),
    product_repo: IProductRepo = Depends(product_repo_depend),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(user_auth_depend),
): 
    try:
        get_product_usecase = GetProduct(product_repo, category_repo)
        output = await get_product_usecase.execute(product_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
