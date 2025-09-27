from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.usecases.category.create_category import CreateCategory
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.category_repo_depend import get_category_repo
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/create",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_category(
    category: CreateCategoryInput = Query(...),
    category_repo: ICategoryRepo = Depends(get_category_repo),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        create_category_usecase = CreateCategory(category_repo)
        output = await create_category_usecase.execute(category)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
