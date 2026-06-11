import grpc
from google.protobuf.json_format import MessageToDict, ParseDict

from sharedlib.grpc.service.order import user_order_service_pb2
from sharedlib.grpc.service.order import user_order_service_pb2_grpc

from src.gateway.internal.interface.Iorder_service import IOrderService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
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
        self.stub = user_order_service_pb2_grpc.IOrderServiceStub(channel)
    
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
  
            response: user_order_service_pb2.PlaceOrderResponse = self.stub.place_order(
                ParseDict(order.model_dump(mode="json"), user_order_service_pb2.PlaceOrderInput()),
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
            
            response: user_order_service_pb2.GetByIdResponse = self.stub.get_by_id(
                ParseDict(params, user_order_service_pb2.GetByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())

    async def update(
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

            response: user_order_service_pb2.UpdateResponse = self.stub.update(
                ParseDict(order.model_dump(mode="json"), user_order_service_pb2.UpdateOrderInput()),
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
            
            response: user_order_service_pb2.GetByCriteriaResponse = self.stub.get_by_criteria(
                ParseDict(criteria.model_dump(mode="json"), user_order_service_pb2.OrderFilterInput()),
                metadata=metadata,
            )
            return [ MessageToDict(item) for item in response.return_value.items()]
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())