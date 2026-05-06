from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.usecases.category.delete_by_parent_id import DeleteCategoriesByParentId
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/all/by-parent-id",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_parent_id(
    parent_id: str = Query(...),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
):
    try:
        delete_category_usecase = DeleteCategoriesByParentId(category_repo)
        output = await delete_category_usecase.execute(parent_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
