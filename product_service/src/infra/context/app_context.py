from src.domain.enums import ServiceCommunication
from src.infra.schemas.broker.nats import NatsClient
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from typing import ClassVar
from aiohttp import ClientSession

class AppContext(type):
    
    auth_base_url: ClassVar[str] = None
    
    auth_communication_type: ClassVar[ServiceCommunication] = None
    
    broker_client: ClassVar[NatsClient] = None
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    http_client: ClassVar[ClientSession] = None