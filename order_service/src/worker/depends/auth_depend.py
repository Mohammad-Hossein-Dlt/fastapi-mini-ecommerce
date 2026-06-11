from .depend import Depends
from grpc import aio
from faststream import StreamMessage
from faststream import Context
from src.infra.context.app_context import AppContext
from src.infra.auth.jwt_handler import JWTHandler
from src.gateway.internal.interface.Iauth_service import IAuthService
from .internal_service_depend import auth_service_depend
from src.dto.schemas.user.user_model import UserModel
from src.usecases.admin.self.get import GetAdmin
from src.usecases.user.self.get import GetUser
from src.infra.exceptions.exceptions import AppBaseException
from functools import partial
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    contextT = aio.ServicerContext
else:
    contextT = Any

def token_from_broker_message_depend(
    msg: StreamMessage = Context("message"),
) -> str:
    
    token = msg.headers.get("token", None)
    if not token:
        raise AppBaseException(status_code=401, message="Missing authorization header")
    
    return token

def token_from_grpc_metadata_depend(
    context: contextT,
) -> str:
    
    metadata = dict(context.invocation_metadata())
    token = metadata.get("authorization", None)
    if not token:
        raise AppBaseException(status_code=401, message="Missing authorization header")
    
    return token

def token_depend():

    if AppContext.order_communication_type == "broker":
        return partial(token_from_broker_message_depend)
    elif AppContext.order_communication_type == "grpc":
        return partial(token_from_grpc_metadata_depend)

def jwt_handler_depend() -> JWTHandler:
    jwt_handler = JWTHandler()
    return jwt_handler

async def verify_token_depend(
    token: str = Depends(token_depend()),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
) -> UserModel:
    
    return jwt_handler.is_token_valid(token)
 

async def admin_auth_depend(
    token: str = Depends(token_depend()),
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
    token: str = Depends(token_depend()),
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