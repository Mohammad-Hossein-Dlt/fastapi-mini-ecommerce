from src.infra.schemas.broker.rabbitmq import RabbitClient
from typing import ClassVar
from aiohttp import ClientSession

class AppContext(type):
    
    auth_base_url: ClassVar[str] = None
    product_base_url: ClassVar[str] = None
    order_base_url: ClassVar[str] = None
    broker_client: ClassVar[RabbitClient] = None
    http_client: ClassVar[ClientSession] = None
