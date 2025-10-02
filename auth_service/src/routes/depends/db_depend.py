from sqlalchemy.orm import sessionmaker, Session
from motor.motor_asyncio import AsyncIOMotorClient
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
from typing import Generator, Union

def get_db_depend() -> Generator[Union[Session, AsyncIOMotorClient], None, None]:
    
    db_client: AsyncIOMotorClient | sessionmaker = get_app_state(app, AppStates.DB_CLIENT)
    
    if isinstance(db_client, sessionmaker):
        session: Session = db_client()
        try:
            yield session
        finally:
            session.close()
    
    if isinstance(db_client, AsyncIOMotorClient):
        yield db_client