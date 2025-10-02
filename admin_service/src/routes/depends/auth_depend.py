from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from src.infra.auth.jwt_handler import JWTHandler
from src.infra.external_api.interface.Iauth_service import IAuthService
from .external_api_services_depend import get_auth_service
from src.repo.interface.Iauth_repo import IAuthRepo
from .auth_repo_depend import get_auth_repo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.usecases.auth.refresh_token import RefreshToken
from src.usecases.admin.self.admin_get_self import AdminGetSelf
from src.infra.exceptions.exceptions import AppBaseException
from typing import Annotated

bearer = HTTPBearer()

def get_jwt_handler() -> JWTHandler:
    jwt_handler = JWTHandler()
    return jwt_handler

async def admin_auth_depend(
    bearer_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    auth_service: IAuthService = Depends(get_auth_service),
    auth_repo: IAuthRepo = Depends(get_auth_repo),
) -> UserModel:
    
    try:
        credentials: AuthCredentials = auth_repo.get_user_auth_credentials()
    except AppBaseException as credentials_ex:
        raise HTTPException(status_code=credentials_ex.status_code, detail=credentials_ex.message)
    
    try:
        jwt_handler.is_token_valid(bearer_token.credentials)
        print("Current access token is valid")
    except AppBaseException:
            try:
                refresh_token_usecase = RefreshToken(auth_service, auth_repo)
                credentials = await refresh_token_usecase.execute(credentials)
                print("Token refreshed using refresh_token")
            except AppBaseException as refresh_ex:
                raise HTTPException(status_code=refresh_ex.status_code, detail=refresh_ex.message)
                
    try:
        get_user_usecase = AdminGetSelf(auth_service)
        user = await get_user_usecase.execute(credentials)
        user.credentials = auth_repo.get_user_auth_credentials()
        return user
    except AppBaseException as get_user_ex:
        raise HTTPException(status_code=get_user_ex.status_code, detail=get_user_ex.message)