import grpc
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.empty_pb2 import Empty

from sharedlib.grpc.service.category import category_service_pb2
from sharedlib.grpc.service.category import category_service_pb2_grpc

from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.category.create_category_input import CreateCategoryInput
from src.schemas.category.update_category_input import UpdateCategoryInput
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer
from src.infra.utils.grpc_status_code import grpc_to_rest_status

class CategoryGrpcService(ICategoryService):
    
    def __init__(
        self,
        channel: grpc.Channel,
    ):
        self.stub = category_service_pb2_grpc.ICategoryServiceStub(channel)
    
    async def create(
        self,
        credentials: AuthCredentials,
        category: CreateCategoryInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: category_service_pb2.CreateResponse = self.stub.create(
                ParseDict(category.model_dump(mode="json"), category_service_pb2.CreateCategoryInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())

    async def get_by_id(
        self,
        credentials: AuthCredentials,
        category_id: str,
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
                    "category_id": category_id,
                },
                mode="grpc",
            )

            response: category_service_pb2.GetByIdResponse = self.stub.get_by_id(
                ParseDict(params, category_service_pb2.GetByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())
          
    async def update(
        self,
        credentials: AuthCredentials,
        category: UpdateCategoryInput,
    ) -> dict:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: category_service_pb2.UpdateResponse = self.stub.update(
                ParseDict(category.model_dump(mode="json"), category_service_pb2.UpdateCategoryInput()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())

    async def delete_by_id(
        self,
        credentials: AuthCredentials,
        category_id: str,
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
                    "category_id": category_id,
                },
                mode="grpc",
            )
            
            response: category_service_pb2.DeleteByIdResponse = self.stub.delete_by_id(
                ParseDict(params, category_service_pb2.DeleteByIdRequest()),
                metadata=metadata,
            )
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())    

    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: CategoryFilterInput,
    ) -> list:
        
        try:
            metadata = outbound_serializer(
                [
                    ("authorization", credentials.access_token),
                ],
                mode="grpc",
            )
            
            response: category_service_pb2.GetByCriteriaResponse = self.stub.get_by_criteria(
                ParseDict(criteria.model_dump(mode="json"), category_service_pb2.CategoryFilterInput()),
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
            
            response: category_service_pb2.DeleteAllResponse = self.stub.delete_all(Empty(), metadata=metadata)
            return MessageToDict(response.return_value)
        except grpc.RpcError as e:
            raise AppBaseException(grpc_to_rest_status(e.code()), e.details())