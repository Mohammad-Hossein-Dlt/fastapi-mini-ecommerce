from faststream import Depends
from .db_depend import db_depend

from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient

from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.postgresql.product_pg_repo import ProductPgRepo
from src.repo.mongodb.product_mongodb_repo import ProductMongodbRepo

def product_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)    
) -> IProductRepo:
        
    if isinstance(db_client, Session):
        return ProductPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return ProductMongodbRepo()