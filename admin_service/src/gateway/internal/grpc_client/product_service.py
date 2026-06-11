import grpc
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.empty_pb2 import Empty

from sharedlib.grpc.service.product import product_service_pb2
from sharedlib.grpc.service.product import product_service_pb2_grpc

from src.gateway.internal.interface.Iproduct_service import IProductService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.product.create_product_input import CreateProductInput
from src.schemas.product.update_product_input import UpdateProductInput
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
    
    async def create(
        self,
        credentials: AuthCredentials,
        product: CreateProductInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )

            response: product_service_pb2.CreateResponse = self.stub.create(
                ParseDict(product.model_dump(mode="json"), product_service_pb2.CreateProductInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
        
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
    
    async def update(
        self,
        credentials: AuthCredentials,
        product: UpdateProductInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: product_service_pb2.UpdateResponse = self.stub.update(
                ParseDict(product.model_dump(mode="json"), product_service_pb2.UpdateProductInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())

    async def delete_by_id(
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
            
            response: product_service_pb2.DeleteByIdResponse = self.stub.delete_by_id(
                ParseDict(params, product_service_pb2.DeleteByIdRequest()),
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
                                        
    async def delete_all(
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
            
            response: product_service_pb2.DeleteAllResponse = self.stub.delete_all(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())