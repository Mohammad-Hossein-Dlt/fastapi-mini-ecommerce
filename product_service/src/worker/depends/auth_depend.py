from faststream import StreamMessage
from faststream import Context
from faststream import Depends
from src.infra.auth.jwt_handler import JWTHandler
from src.gateway.internal.interface.Iauth_service import IAuthService
from .internal_http_depend import auth_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.usecases.admin.get import GetAdmin
from src.usecases.user.get import GetUser
from src.infra.exceptions.exceptions import AppBaseException

def token_from_message_depend(
    msg: StreamMessage = Context("message"),
) -> str:
    
    token = msg.headers.get("token", None)
    if not token:
        raise AppBaseException(status_code=401, message="Missing authorization header")
    
    return token

def jwt_handler_depend() -> JWTHandler:
    jwt_handler = JWTHandler()
    return jwt_handler

async def verify_token_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
) -> UserModel:
    
    return jwt_handler.is_token_valid(token)
 

async def admin_auth_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    auth_service: IAuthService = Depends(auth_service_depend),
) -> UserModel:
    
    token = await verify_token_depend(
        token,
        jwt_handler,
    )
        
    get_user_usecase = GetAdmin(auth_service)
    user = await get_user_usecase.execute(token)
    user.token = token
    return user    
    
async def user_auth_depend(
    token: str = Depends(token_from_message_depend),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    auth_service: IAuthService = Depends(auth_service_depend),
) -> UserModel:
    
    token = await verify_token_depend(
        token,
        jwt_handler,
    )
        
    get_user_usecase = GetUser(auth_service)
    user = await get_user_usecase.execute(token)
    user.token = token
    return user