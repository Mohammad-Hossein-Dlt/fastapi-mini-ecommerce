from fastapi import Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from .db_depend import db_depend

from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.postgresql.category_pg_repo import CategoryPgRepo
from src.repo.mongodb.category_mongodb_repo import CategoryMongodbRepo

def category_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)    
) -> ICategoryRepo:
        
    if isinstance(db_client, Session):
        return CategoryPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return CategoryMongodbRepo()