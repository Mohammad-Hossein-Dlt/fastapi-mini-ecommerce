import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty

from sharedlib.grpc.service.auth import admin_service_pb2
from sharedlib.grpc.service.auth import admin_service_pb2_grpc

from sharedlib.grpc.service.auth import user_service_pb2
from sharedlib.grpc.service.auth import user_service_pb2_grpc

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer
from src.infra.utils.grpc_status_code import grpc_to_rest_status

class AuthGrpcService(IAuthService):
    
    def __init__(
        self,
        channel: grpc.Channel,
    ):
        self.admin_stub = admin_service_pb2_grpc.IAdminServiceStub(channel)
        self.user_stub = user_service_pb2_grpc.IUserServiceStub(channel)
    
    async def get_admin(
        self,
        access_token: str,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", access_token),
                ],
                mode="grpc",
            )
        
            response: admin_service_pb2.GetSelfResponse = self.admin_stub.get_self(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def get_user(
        self,
        access_token: str,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", access_token),
                ],
                mode="grpc",
            )
            
            response: user_service_pb2.GetSelfResponse = self.user_stub.get_self(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())