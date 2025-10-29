from pydantic import BaseModel, ConfigDict

class KafkaParams(BaseModel):
    pass

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
