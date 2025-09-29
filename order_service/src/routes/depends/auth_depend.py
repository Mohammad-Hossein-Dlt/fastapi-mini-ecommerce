from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from src.infra.auth.jwt_handler import JWTHandler
from src.infra.external_api.interface.Iauth_service import IAuthService
from .external_api_services_depend import get_auth_service
from src.domain.schemas.user.user_model import UserModel
from src.usecases.admin.self.admin_get_self import AdminGetSelf
from src.usecases.user.self.user_get_self import UserGetSelf
from src.infra.exceptions.exceptions import AppBaseException, InvalidTokenException
from typing import Annotated

bearer = HTTPBearer()

def get_jwt_handler() -> JWTHandler:
    jwt_handler = JWTHandler()
    return jwt_handler

async def verify_token_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
) -> UserModel:
    
    try:
        return jwt_handler.is_token_valid(bearer_token.credentials)
    except InvalidTokenException as access_ex:
        raise HTTPException(status_code=access_ex.status_code, detail=access_ex.message)  

async def admin_auth_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    auth_service: IAuthService = Depends(get_auth_service),
) -> UserModel:
    
    token = await verify_token_depend(
        bearer_token,
        jwt_handler,
    )
        
    get_user_usecase = AdminGetSelf(auth_service)
    try:
        user = get_user_usecase.execute(token)
        user.token = bearer_token.credentials
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)
    
    
async def user_auth_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    auth_service: IAuthService = Depends(get_auth_service),
) -> UserModel:
    
    token = await verify_token_depend(
        bearer_token,
        jwt_handler,
    )
        
    get_user_usecase = UserGetSelf(auth_service)
    try:
        user = get_user_usecase.execute(token)
        user.token = bearer_token.credentials
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)