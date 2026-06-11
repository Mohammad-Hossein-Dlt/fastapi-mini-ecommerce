from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.routes.depends.internal_service_depend import category_service_depend
from src.dto.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.category.get_by_criteria import GetCategories
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_criteria(
    criteria: CategoryFilterInput = Query(...),
    category_service: ICategoryService = Depends(category_service_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_all_user_categorys_usecase = GetCategories(category_service)
        outputs_list = await get_all_user_categorys_usecase.execute(user.credentials, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
