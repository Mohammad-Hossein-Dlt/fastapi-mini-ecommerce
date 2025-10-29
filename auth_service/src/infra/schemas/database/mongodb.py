from pydantic import BaseModel, ConfigDict
from motor.motor_asyncio import AsyncIOMotorClient

class MongodbParams(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class MongodbClient(BaseModel):
    client: AsyncIOMotorClient

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
