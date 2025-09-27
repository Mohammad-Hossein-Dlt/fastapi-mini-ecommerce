from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.routes.depends.external_api_services_depend import get_category_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.category.update_category import UpdateCategory
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/update/one",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_category(
    category: UpdateCategoryInput = Query(...),
    category_service: ICategoryService = Depends(get_category_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        update_category_usecase = UpdateCategory(category_service)
        output = await update_category_usecase.execute(user.credentials, category)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
