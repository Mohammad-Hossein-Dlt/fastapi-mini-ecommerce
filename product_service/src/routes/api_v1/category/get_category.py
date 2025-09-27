from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.category.get_category import GetCategory
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
async def get_category(
    category_id: str = Query(...),
    category_repo: ICategoryRepo = Depends(get_category_repo),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_category_usecase = GetCategory(category_repo)
        output = await get_category_usecase.execute(category_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
