from fastapi import Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from .db_depend import get_db_depend
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.repo.mongodb.admin.order_mongodb_repo import AdminOrderMongodbRepo
from src.repo.postgresql.admin.order_pg_repo import AdminPgRepo

from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.repo.mongodb.user.order_mongodb_repo import OrderMongodbRepo
from src.repo.postgresql.user.order_pg_repo import OrderPgRepo

    
def get_admin_order_repo(
    db_client: AsyncIOMotorClient | Session = Depends(get_db_depend)
) -> IAdminOrderRepo:
    
    if isinstance(db_client, AsyncIOMotorClient):
        return AdminOrderMongodbRepo()
    
    
    if isinstance(db_client, Session):
        return AdminPgRepo(db_client)

def get_user_order_repo(
    db_client: AsyncIOMotorClient | Session = Depends(get_db_depend)    
) -> IOrderRepo:
    
    if isinstance(db_client, AsyncIOMotorClient):
        return OrderMongodbRepo()
    
    if isinstance(db_client, Session):
        return OrderPgRepo(db_client)