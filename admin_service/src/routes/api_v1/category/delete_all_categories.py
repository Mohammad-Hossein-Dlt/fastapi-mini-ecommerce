from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.routes.depends.external_api_services_depend import get_category_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.category.delete_all_categories import DeleteAllCategories
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_all_categories(
    category_service: ICategoryService = Depends(get_category_service),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_category_usecase = DeleteAllCategories(category_service)
        output = await delete_all_category_usecase.execute(user.credentials)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
