from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.category.delete_category import DeleteCategory
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.category_repo_depend import get_category_repo
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
async def delete_one_category(
    category_id: str = Query(...),
    category_repo: ICategoryRepo = Depends(get_category_repo),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_category_usecase = DeleteCategory(category_repo)
        output = await delete_category_usecase.execute(category_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
