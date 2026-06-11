from .depend import Depends
from .db_depend import db_client_depend

from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient

from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.repo.mongodb.admin.order_mongodb_repo import AdminOrderMongodbRepo
from src.repo.postgresql.admin.order_pg_repo import AdminPgRepo

from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.repo.mongodb.user.order_mongodb_repo import OrderMongodbRepo
from src.repo.postgresql.user.order_pg_repo import OrderPgRepo

def admin_order_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IAdminOrderRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return AdminOrderMongodbRepo()
    
    if isinstance(db_client, Session):
        return AdminPgRepo(db_client)

def user_order_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)    
) -> IOrderRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return OrderMongodbRepo()
    
    if isinstance(db_client, Session):
        return OrderPgRepo(db_client)