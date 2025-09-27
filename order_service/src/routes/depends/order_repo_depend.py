from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.repo.interface.user.Iorder_repo import IOrderRepo
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from src.infra.fastapi_config.app import app
from src.infra.fastapi_config.app_state import AppStates, get_app_state
# from src.repo.postgresql.order_pg_repo import orderPgRepo
from src.repo.mongodb.user.order_mongodb_repo import OrderMongodbRepo
from src.repo.mongodb.admin.order_mongodb_repo import AdminOrderMongodbRepo

    
def get_admin_order_repo() -> IAdminOrderRepo:
    
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    
    # if isinstance(db_client, Session):
    #     return orderPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return AdminOrderMongodbRepo()

def get_order_repo() -> IOrderRepo:
    
    db_client: AsyncIOMotorClient | Session = get_app_state(app, AppStates.DB_CLIENT)
    
    # if isinstance(db_client, Session):
    #     return orderPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return OrderMongodbRepo()
