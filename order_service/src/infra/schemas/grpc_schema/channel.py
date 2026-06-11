from pydantic import BaseModel, ConfigDict
import grpc

class GrpcChannel(BaseModel):
    channel: grpc.Channel

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
