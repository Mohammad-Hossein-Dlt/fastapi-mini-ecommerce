from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.infra.external_api.interface.Iauth_service import IAuthService
from src.routes.depends.external_api_services_depend import get_auth_service
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.user.self.user_get_self import UserGetSelf
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/get",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def user_get_self(
    auth_service: IAuthService = Depends(get_auth_service),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_user_usecase = UserGetSelf(auth_service)
        return get_user_usecase.execute(user.credentials)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
