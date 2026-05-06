from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.routes.depends.internal_http_depend import category_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.category.get_by_id import GetCategory
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_id(
    category_id: str = Query(...),
    category_service: ICategoryService = Depends(category_service_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_category_usecase = GetCategory(category_service)
        output = await get_category_usecase.execute(user.credentials, category_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
