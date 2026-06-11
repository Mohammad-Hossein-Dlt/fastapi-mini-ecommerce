from pydantic import BaseModel, ConfigDict

class GrpcParams(BaseModel):
    url: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )