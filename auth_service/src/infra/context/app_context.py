from typing import ClassVar
from src.dto.enums import ServiceCommunication
from src.infra.schemas.broker.nats import NatsClient
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from src.infra.auth.jwt_handler import JWTHandler
from aiohttp import ClientSession

class AppContext(type):
    
    auth_communication_type: ClassVar[ServiceCommunication] = None
    product_communication_type: ClassVar[ServiceCommunication] = None
    order_communication_type: ClassVar[ServiceCommunication] = None    
    
    broker_client: ClassVar[NatsClient] = None
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    http_client: ClassVar[ClientSession] = None
    jwt: ClassVar[JWTHandler] = None