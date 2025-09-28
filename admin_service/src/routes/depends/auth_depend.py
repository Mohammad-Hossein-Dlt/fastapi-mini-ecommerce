from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from src.infra.auth.jwt_handler import JWTHandler
from src.infra.external_api.interface.Iauth_service import IAuthService
from .external_api_services_depend import get_auth_service
from src.domain.schemas.user.user_model import UserModel
from src.usecases.admin.self.admin_get_self import AdminGetSelf
from src.repo.interface.Iauth_repo import IAuthRepo
from .auth_repo_depend import get_auth_repo
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
    auth_repo: IAuthRepo = Depends(get_auth_repo),
) -> UserModel:
    
    await verify_token_depend(
        bearer_token,
        jwt_handler,
    )
        
    try:
        get_user_usecase = AdminGetSelf(auth_service)
        user = get_user_usecase.execute(auth_repo.get_user_auth_credentials())
        user.credentials = auth_repo.get_user_auth_credentials()
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)