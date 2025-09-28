from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.routes.depends.external_api_services_depend import get_category_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.category.get_all_categories import GetAllCategories
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_categories(
    category_filter: CategoryFilterInput = Query(...),
    category_service: ICategoryService = Depends(get_category_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_all_user_categorys_usecase = GetAllCategories(category_service)
        outputs_list = await get_all_user_categorys_usecase.execute(user.credentials, category_filter)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
