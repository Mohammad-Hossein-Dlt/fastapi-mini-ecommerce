from ._router import router 
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.routes.depends.internal_http_depend import auth_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.routes.depends.auth_depend import user_auth_depend
from src.usecases.user.self.user_delete_self import UserDeleteSelf
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/delete",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def user_delete_self(
    auth_service: IAuthService = Depends(auth_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        delete_user_usecase = UserDeleteSelf(auth_service)
        output = await delete_user_usecase.execute(user.credentials)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))