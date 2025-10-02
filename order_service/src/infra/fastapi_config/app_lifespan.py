from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.db.mongodb.client import init_mongodb
from src.infra.settings.settings import settings
from src.infra.db.postgresql.database import init_sql_client, create_tables
from .app_state import AppStates, set_app_state
from motor.motor_asyncio import AsyncIOMotorClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient()
    
    if settings.ORDER_DB_STACK == "postgresql":
        sql_client, engine = init_sql_client(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            db_name=settings.POSTGRES_DB
        )
        create_tables(engine)
        
        set_app_state(app, AppStates.DB_CLIENT, sql_client)
        
    if settings.ORDER_DB_STACK == "mongo_db":
        mongo_client = await init_mongodb(
            host=settings.MONGO_HOST,
            port=settings.MONGO_PORT,
            username=settings.MONGO_INITDB_ROOT_USERNAME,
            password=settings.MONGO_INITDB_ROOT_PASSWORD,
            db_name=settings.MONGO_INITDB_DATABASE,
        )
        set_app_state(app, AppStates.DB_CLIENT, mongo_client)
    
        
    set_app_state(app, AppStates.EXTERNAL_FASTAPI_PORT, settings.EXTERNAL_FASTAPI_PORT)
    set_app_state(app, AppStates.INTERNAL_FASTAPI_PORT, settings.INTERNAL_FASTAPI_PORT)
    
    set_app_state(app, AppStates.AUTH_BASE_URL, settings.AUTH_BASE_URL)
    set_app_state(app, AppStates.PRODUCT_BASE_URL, settings.PRODUCT_BASE_URL)
            
    yield
    
    mongo_client.close()
    
