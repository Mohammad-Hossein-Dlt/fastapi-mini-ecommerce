from ._router import router 
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.routes.depends.internal_service_depend import auth_service_depend
from src.dto.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import admin_auth_depend
from src.usecases.admin.user.get_user import GetUser
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_user(
    user_id: str = Query(None),
    username: str = Query(None),
    auth_service: IAuthService = Depends(auth_service_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_user_usecase = GetUser(auth_service)
        output = await get_user_usecase.execute(user.credentials, user_id, username)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
