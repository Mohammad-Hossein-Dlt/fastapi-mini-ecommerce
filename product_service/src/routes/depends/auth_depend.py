from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from src.infra.auth.jwt_handler import JWTHandler
from src.gateway.internal.interface.Iauth_service import IAuthService
from .internal_http_depend import auth_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.usecases.admin.admin_get_self import AdminGetSelf
from src.usecases.user.user_get_self import UserGetSelf
from src.infra.exceptions.exceptions import AppBaseException, InvalidTokenException
from typing import Annotated

token_schema = HTTPBearer()

def jwt_handler_depend() -> JWTHandler:
    jwt_handler = JWTHandler()
    return jwt_handler

async def verify_token_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(token_schema)],
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
) -> UserModel:
    
    try:
        return jwt_handler.is_token_valid(bearer_token.credentials)
    except InvalidTokenException as access_ex:
        raise HTTPException(status_code=access_ex.status_code, detail=access_ex.message)  

async def admin_auth_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(token_schema)],
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    auth_service: IAuthService = Depends(auth_service_depend),
) -> UserModel:
    
    token = await verify_token_depend(
        bearer_token,
        jwt_handler,
    )
        
    get_user_usecase = AdminGetSelf(auth_service)
    try:
        user = await get_user_usecase.execute(token)
        user.token = bearer_token.credentials
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)
    
    
async def user_auth_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(token_schema)],
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    auth_service: IAuthService = Depends(auth_service_depend),
) -> UserModel:
    
    token = await verify_token_depend(
        bearer_token,
        jwt_handler,
    )
        
    get_user_usecase = UserGetSelf(auth_service)
    try:
        user = await get_user_usecase.execute(token)
        user.token = bearer_token.credentials
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)