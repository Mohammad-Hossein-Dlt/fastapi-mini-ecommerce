from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

class SqlalchemyParams(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class SqlalchemyClient(BaseModel):
    engine: Engine
    client: sessionmaker

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

