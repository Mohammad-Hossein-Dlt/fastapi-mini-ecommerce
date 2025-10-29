from typing import ClassVar
from src.infra.schemas.broker.rabbitmq_params import RabbitParams
from src.infra.schemas.broker.kafka_params import KafkaParams
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from aiohttp import ClientSession

class AppContext(type):
    
    auth_base_url: ClassVar[str] = None
    
    broker_params: ClassVar[RabbitParams | KafkaParams] = None
    
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    
    http_client: ClassVar[ClientSession] = None