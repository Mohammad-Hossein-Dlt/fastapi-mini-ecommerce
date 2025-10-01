from fastapi import Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from .db_depend import get_db_depend
from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.postgresql.product_pg_repo import ProductPgRepo
from src.repo.mongodb.product_mongodb_repo import ProductMongodbRepo

def get_product_repo(
    db_client: AsyncIOMotorClient | Session = Depends(get_db_depend)    
) -> IProductRepo:
        
    if isinstance(db_client, Session):
        return ProductPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return ProductMongodbRepo()