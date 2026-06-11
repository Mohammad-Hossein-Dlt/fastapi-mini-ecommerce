import grpc
from google.protobuf.json_format import MessageToDict, ParseDict

from sharedlib.grpc.service.order import admin_order_service_pb2
from sharedlib.grpc.service.order import admin_order_service_pb2_grpc

from sharedlib.grpc.service.order import user_order_service_pb2
from sharedlib.grpc.service.order import user_order_service_pb2_grpc

from src.gateway.internal.interface.Iorder_service import IOrderService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.order.modify_order_input import ModifyOrderInput
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.schemas.order.place_order_input import PlaceOrderInput
from src.schemas.order.update_order_input import UpdateOrderInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer
from src.infra.utils.grpc_status_code import grpc_to_rest_status

class OrderGrpcService(IOrderService):
    
    def __init__(
        self,
        channel: grpc.Channel,
    ):
        self.admin_stub = admin_order_service_pb2_grpc.IOrderServiceStub(channel)
        self.user_stub = user_order_service_pb2_grpc.IOrderServiceStub(channel)
    
    async def modify(
        self,
        credentials: AuthCredentials,
        modify: ModifyOrderInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: admin_order_service_pb2.ModifyResponse = self.admin_stub.modify(
                ParseDict(modify.model_dump(mode="json"), admin_order_service_pb2.ModifyOrderInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
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
                    "order_id": order_id,
                },
                mode="grpc",
            )
            
            response: admin_order_service_pb2.GetByIdResponse = self.admin_stub.get_by_id(
                ParseDict(params, admin_order_service_pb2.GetByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def delete_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
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
                    "order_id": order_id,
                },
                mode="grpc",
            )
            
            response: admin_order_service_pb2.DeleteByIdResponse = self.admin_stub.delete_by_id(
                ParseDict(params, admin_order_service_pb2.DeleteByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
                
    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )

            response: admin_order_service_pb2.GetByCriteriaResponse = self.admin_stub.get_by_criteria(
                ParseDict(criteria.model_dump(mode="json"), admin_order_service_pb2.OrderFilterInput()),
                metadata=metadata,
            )
            return [ MessageToDict(item) for item in response.return_value.items()]
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
            
    async def delete_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )

            response: admin_order_service_pb2.DeleteByCriteriaResponse = self.admin_stub.delete_by_criteria(
                ParseDict(criteria.model_dump(mode="json"), admin_order_service_pb2.OrderFilterInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def place_order(
        self,
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
  
            response: user_order_service_pb2.PlaceOrderResponse = self.user_stub.place_order(
                ParseDict(order.model_dump(mode="json"), user_order_service_pb2.PlaceOrderInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def user_get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
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
                    "order_id": order_id,
                },
                mode="grpc",
            )
            
            response: user_order_service_pb2.GetByIdResponse = self.user_stub.get_by_id(
                ParseDict(params, user_order_service_pb2.GetByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
    
    async def user_update(
        self,
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:

        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )

            response: user_order_service_pb2.UpdateResponse = self.user_stub.update(
                ParseDict(order.model_dump(mode="json"), user_order_service_pb2.UpdateOrderInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
                
    async def user_get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: user_order_service_pb2.GetByCriteriaResponse = self.user_stub.get_by_criteria(
                ParseDict(criteria.model_dump(mode="json"), user_order_service_pb2.OrderFilterInput()),
                metadata=metadata,
            )
            return [ MessageToDict(item) for item in response.return_value.items()]
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())