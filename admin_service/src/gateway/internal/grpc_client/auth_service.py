import grpc
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.empty_pb2 import Empty

from sharedlib.grpc.service.auth import auth_service_pb2
from sharedlib.grpc.service.auth import auth_service_pb2_grpc

from sharedlib.grpc.service.auth import admin_service_pb2
from sharedlib.grpc.service.auth import admin_service_pb2_grpc

from sharedlib.grpc.service.auth import user_service_pb2
from sharedlib.grpc.service.auth import user_service_pb2_grpc

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.schemas.user.user_register_input import UserRegisterInput
from src.schemas.user.user_login_input import UserLoginInput
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.dto.enums import Role
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer
from src.infra.utils.enum_index import get_index
from src.infra.utils.grpc_status_code import grpc_to_rest_status

class AuthGrpcService(IAuthService):
    
    def __init__(
        self,
        channel: grpc.Channel,
    ):
        self.auth_stub = auth_service_pb2_grpc.IAuthServiceStub(channel)
        self.admin_stub = admin_service_pb2_grpc.IAdminServiceStub(channel)
        self.user_stub = user_service_pb2_grpc.IUserServiceStub(channel)
        
    async def register(
        self,
        user: UserRegisterInput,
    ) -> dict:
        
        try:
            user: dict = user.model_dump(mode="json")
            user["role"] = get_index(Role, Role.ADMIN)
            response: auth_service_pb2.RegisterResponse = self.auth_stub.register(
                ParseDict(user, auth_service_pb2.RegisterInput()),
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
        
    async def login(
        self,
        user: UserLoginInput,
    ) -> dict:
        
        try:
            response: auth_service_pb2.LoginResponse = self.auth_stub.login(
                ParseDict(user.model_dump(mode="json"), auth_service_pb2.LoginInput()),
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
            
    async def refresh_token(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.refresh_token),
                ],
                mode="grpc",
            )
            
            response: auth_service_pb2.RefreshTokenResponse = self.auth_stub.refresh_token(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def admin_get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )

            response: admin_service_pb2.GetSelfResponse = self.admin_stub.get_self(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def admin_get_user(
        self,
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            params = outbound_serializer(
                {
                    "user_id": user_id,
                    "username": username,
                },
                mode="grpc",
            )
 
            response: admin_service_pb2.GetUserResponse = self.admin_stub.get_user(
                ParseDict(params, admin_service_pb2.GetUserRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def admin_delete_user(
        self,
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            params = outbound_serializer(
                {
                    "user_id": user_id,
                    "username": username,
                },
                mode="grpc",
            )

            response: admin_service_pb2.DeleteUserResponse = self.admin_stub.delete_user(
                ParseDict(params, admin_service_pb2.DeleteUserRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
            
    async def user_get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: user_service_pb2.GetSelfResponse = self.user_stub.get_self(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def user_delete_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
            
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: user_service_pb2.DeleteSelfResponse = self.user_stub.delete_self(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())