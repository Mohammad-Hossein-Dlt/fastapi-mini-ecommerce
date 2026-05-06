from src.infra.context.app_context import AppContext
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Generator, Union

def db_client_depend() -> Generator[Union[Session, AsyncIOMotorClient], None, None]:
    client = AppContext.db_client
    yield from client.get_dependency()