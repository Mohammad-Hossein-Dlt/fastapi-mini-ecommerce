from fastapi import Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from .db_depend import get_db_depend
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.postgresql.category_pg_repo import CategoryPgRepo
from src.repo.mongodb.category_mongodb_repo import CategoryMongodbRepo

def get_category_repo(
    db_client: AsyncIOMotorClient | Session = Depends(get_db_depend)    
) -> ICategoryRepo:
        
    if isinstance(db_client, Session):
        return CategoryPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return CategoryMongodbRepo()