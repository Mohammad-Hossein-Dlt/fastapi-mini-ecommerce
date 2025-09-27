from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
from src.infra.auth.jwt_handler import JWTHandler
from .user_repo_depend import get_user_repo
from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.usecases.user.user_get_self import UserGetSelf
from src.domain.enums import Role
from src.infra.exceptions.exceptions import AppBaseException, InvalidTokenException

schema = OAuth2PasswordBearer(tokenUrl="/auth/api/v1/login")

def jwt_handler_depend() -> JWTHandler:
    
    secret = get_app_state(app, AppStates.JWT_SECRET)
    algorithm = get_app_state(app, AppStates.JWT_ALGORITHM)
    jwt_expiration_minutes = get_app_state(app, AppStates.JWT_EXPIRATION_MINUTES)
    jwt_refresh_expiration_minutes = get_app_state(app, AppStates.JWT_REFRESH_EXPIRATION_MINUTES)
    
    jwt_handler = JWTHandler(secret, algorithm, jwt_expiration_minutes, jwt_refresh_expiration_minutes)
    
    return jwt_handler

async def auth_depend(
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    token: str = Depends(schema),
    user_repo: IUserRepo = Depends(get_user_repo),
) -> UserModel:
    
    try:
        payload = jwt_handler.decode_jwt_token(token)
    except InvalidTokenException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)
        
    if payload.type == "access":
        get_user_usecase = UserGetSelf(user_repo)
        try:
            return await get_user_usecase.execute(payload.user_id)
        except AppBaseException as ex:
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
            
    elif payload.type == "refresh":
        raise HTTPException(status_code=401, detail="You have not access with refresh-token")
    
    
async def admin_auth_depend(
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    token: str = Depends(schema),
    user_repo: IUserRepo = Depends(get_user_repo),
) -> UserModel:
    user: UserModel = await auth_depend(
        jwt_handler,
        token,
        user_repo,
    )
    if user.role == Role.admin:
        return user
    else:
        raise HTTPException(status_code=401, detail="Only admin have access")