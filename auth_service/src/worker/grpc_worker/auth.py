from grpc import aio
from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty

from sharedlib.grpc.service.auth import auth_service_pb2, auth_service_pb2_grpc

from src.worker.depends.depend import Depends, inject

from src.schemas.user.create_user_input import CreateUserInput
from src.schemas.user.login_user_input import LoginUserInput

from src.infra.auth.jwt_handler import JWTHandler
from src.worker.depends.auth_depend import jwt_handler_depend
from src.repo.interface.Iuser_repo import IUserRepo
from src.worker.depends.repo_depend import user_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import refresh_token_depend

from src.usecases.auth.register import RegisterUser
from src.usecases.auth.login import LoginUser
from src.usecases.auth.refresh_token import RefreshToken

from src.dto.enums import Role
from src.infra.utils.enum_index import get_value_by_index
from src.infra.utils.grpc_status_code import rest_to_grpc_status
from src.infra.exceptions.exceptions import AppBaseException

class AuthServicer(auth_service_pb2_grpc.IAuthService):
    
    @inject(cast=False)
    async def login(
        self,
        request: auth_service_pb2.LoginInput,
        context: aio.ServicerContext,
        user_repo: IUserRepo = Depends(user_repo_depend),
        jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    ):
        try:
            user = LoginUserInput.model_validate(MessageToDict(request, preserving_proto_field_name=True), from_attributes=True)
            create_user_usecase = LoginUser(user_repo, jwt_handler)
            output = await create_user_usecase.execute(user)
            response = output.model_dump(mode="json")
            return auth_service_pb2.LoginResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)

    @inject(cast=False)
    async def register(
        self,
        request: auth_service_pb2.RegisterInput,
        context: aio.ServicerContext,
        user_repo: IUserRepo = Depends(user_repo_depend),
    ):
        try:
            _dict = MessageToDict(request, preserving_proto_field_name=True)
            entity = CreateUserInput(role=get_value_by_index(Role, request.role), **_dict)
            create_user_usecase = RegisterUser(user_repo)
            output = await create_user_usecase.execute(entity)
            response = output.model_dump(mode="json")
            return auth_service_pb2.RegisterResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)
            
    @inject(cast=False)
    async def refresh_token(
        self,
        request: Empty,
        context: aio.ServicerContext,
        jwt_handler: JWTHandler = Depends(jwt_handler_depend),
        user: UserModel = Depends(refresh_token_depend),
    ):
        try:
            refresh_token_usecase = RefreshToken(jwt_handler)
            output = await refresh_token_usecase.execute(user)
            response = output.model_dump(mode="json")
            return auth_service_pb2.RefreshTokenResponse(return_value=response)
        except AppBaseException as e:
            await context.abort(rest_to_grpc_status(e.status_code), e.message)