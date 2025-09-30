from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state

def db_depend() -> AsyncIOMotorClient | Session:
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    return db_client