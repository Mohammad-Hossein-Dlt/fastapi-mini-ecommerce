import grpc
from google.protobuf.json_format import MessageToDict, ParseDict

from sharedlib.grpc.service.product import product_service_pb2
from sharedlib.grpc.service.product import product_service_pb2_grpc

from src.gateway.internal.interface.Iproduct_service import IProductService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.filter.product_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer
from src.infra.utils.grpc_status_code import grpc_to_rest_status

class ProductGrpcService(IProductService):
    
    def __init__(
        self,
        channel: grpc.Channel,
    ):
        self.stub = product_service_pb2_grpc.IProductServiceStub(channel)
        
    async def get_by_id(
        self,
        credentials: AuthCredentials,
        product_id: str,
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
                    "product_id": product_id,
                },
                mode="grpc",
            )
            
            response: product_service_pb2.GetByIdResponse = self.stub.get_by_id(
                ParseDict(params, product_service_pb2.GetByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())

    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: ProductFilterInput,
    ) -> list:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: product_service_pb2.GetByCriteriaResponse = self.stub.get_by_criteria(
                ParseDict(criteria.model_dump(mode="json"), product_service_pb2.ProductFilterInput()),
                metadata=metadata,
            )
            return [ MessageToDict(item) for item in response.return_value.items()]
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())