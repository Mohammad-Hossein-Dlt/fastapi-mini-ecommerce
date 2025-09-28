from src.repo.interface.Iproduct_repo import IProductRepo
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
from src.repo.postgresql.product_pg_repo import ProductPgRepo
from src.repo.mongodb.product_mongodb_repo import ProductMongodbRepo

def get_product_repo() -> IProductRepo:
    
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    
    if isinstance(db_client, Session):
        return ProductPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return ProductMongodbRepo()