from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.user_repo_depend import get_user_repo
from src.usecases.user.user_delete_self import UserDeleteSelf
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_self(
    user: UserModel = Depends(user_auth_depend),
    user_repo: IUserRepo = Depends(get_user_repo),
):
    try:
        delete_user_usecase = UserDeleteSelf(user_repo)
        output = await delete_user_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))