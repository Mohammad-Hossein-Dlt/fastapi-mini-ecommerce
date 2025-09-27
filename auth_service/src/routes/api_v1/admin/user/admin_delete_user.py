from ._router import router 
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.schemas.user.user_model import UserModel
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.auth_depend import admin_auth_depend
from src.routes.depends.user_repo_depend import get_user_repo
from src.usecases.admin.admin_delete_user import AdminDeleteUser
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_user(
    user_id: str = Query(None),
    username: str = Query(None),
    user_repo: IUserRepo = Depends(get_user_repo),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_user_usecase = AdminDeleteUser(user_repo)
        output = await delete_user_usecase.execute(user_id, username)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))