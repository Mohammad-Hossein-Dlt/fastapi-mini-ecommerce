from src.dto.enums import ServiceCommunication
from src.infra.schemas.broker.nats import NatsClient
from src.infra.schemas.grpc_schema.channel import GrpcChannel
from typing import ClassVar
from aiohttp import ClientSession

class AppContext(type):
    
    auth_base_url: ClassVar[str] = None
    product_base_url: ClassVar[str] = None
    order_base_url: ClassVar[str] = None
    
    auth_communication_type: ClassVar[ServiceCommunication] = None
    product_communication_type: ClassVar[ServiceCommunication] = None
    order_communication_type: ClassVar[ServiceCommunication] = None
    
    auth_grpc_channel: ClassVar[GrpcChannel] = None
    product_grpc_channel: ClassVar[GrpcChannel] = None
    order_grpc_channel: ClassVar[GrpcChannel] = None
    
    broker_client: ClassVar[NatsClient] = None
    http_client: ClassVar[ClientSession] = None