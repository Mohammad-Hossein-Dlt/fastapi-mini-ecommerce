from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.usecases.product.get_all_products import GetAllProducts
from src.repo.interface.Iproduct_repo import IProductRepo
from src.routes.depends.product_repo_depend import get_product_repo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.category_repo_depend import get_category_repo
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_categories(
    filter: ProductFilterInput = Query(...),
    product_repo: IProductRepo = Depends(get_product_repo),
    category_repo: ICategoryRepo = Depends(get_category_repo),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_all_user_products_usecase = GetAllProducts(product_repo, category_repo)
        outputs_list = await get_all_user_products_usecase.execute(filter)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
