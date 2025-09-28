from src.repo.interface.Icategory_repo import ICategoryRepo
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
from src.repo.postgresql.category_pg_repo import CategoryPgRepo
from src.repo.mongodb.category_mongodb_repo import CategoryMongodbRepo

def get_category_repo() -> ICategoryRepo:
    
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    
    if isinstance(db_client, Session):
        return CategoryPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return CategoryMongodbRepo()