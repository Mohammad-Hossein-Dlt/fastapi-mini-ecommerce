from pydantic import BaseModel, ConfigDict

class BrokerParams(BaseModel):
    url: str
    exchange: str | None = None    
    queue: str | None = None
    routing_key: str | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
