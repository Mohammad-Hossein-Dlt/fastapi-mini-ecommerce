from .broker_params import BrokerParams
from .broker_client import BaseBrokerClient
from pydantic import BaseModel, ConfigDict
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

class RabbitParams(BrokerParams):
    url: str
    exchange: str    
    queue: str    
    routing_key: str 

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class RabbitClient(BaseBrokerClient, BaseModel):
    params: RabbitParams
    broker: RabbitBroker
    queue: RabbitQueue
    exchange: RabbitExchange
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )