from .broker_params import BrokerParams
from .broker_client import BaseBrokerClient
from pydantic import BaseModel, ConfigDict
from faststream.nats import NatsBroker

class NatsParams(BrokerParams):
    url: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class NatsClient(BaseBrokerClient, BaseModel):
    params: NatsParams
    broker: NatsBroker
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
        
    def get_client_dependency(self):
        yield self.broker