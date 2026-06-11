import grpc
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict, ParseDict

from sharedlib.grpc.service.auth import auth_service_pb2
from sharedlib.grpc.service.auth import auth_service_pb2_grpc

from sharedlib.grpc.service.auth import user_service_pb2
from sharedlib.grpc.service.auth import user_service_pb2_grpc

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.schemas.user.user_register_input import UserRegisterInput
from src.schemas.user.user_login_input import UserLoginInput
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer
from src.infra.utils.grpc_status_code import grpc_to_rest_status

class AuthGrpcService(IAuthService):
    
    def __init__(
        self,
        channel: grpc.Channel,
    ):
        
        self.auth_stub = auth_service_pb2_grpc.IAuthServiceStub(channel)
        self.user_stub = user_service_pb2_grpc.IUserServiceStub(channel)
    
    async def register(
        self,
        user: UserRegisterInput,
    ) -> dict:
        
        try:    
            user: dict = user.model_dump(mode="json")
            user["role"] = "user"
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
    
    async def get_self(
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
        
        except Exception as e:
            print(e)
        
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def delete_self(
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