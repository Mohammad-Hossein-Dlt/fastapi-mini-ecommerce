from faststream import Depends
from .db_depend import db_client_depend

from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient

from src.repo.interface.Iproduct_repo import IProductRepo
from src.repo.postgresql.product_pg_repo import ProductPgRepo
from src.repo.mongodb.product_mongodb_repo import ProductMongodbRepo

from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.postgresql.category_pg_repo import CategoryPgRepo
from src.repo.mongodb.category_mongodb_repo import CategoryMongodbRepo

def product_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)    
) -> IProductRepo:
        
    if isinstance(db_client, Session):
        return ProductPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return ProductMongodbRepo()

def category_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)    
) -> ICategoryRepo:
        
    if isinstance(db_client, Session):
        return CategoryPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return CategoryMongodbRepo()