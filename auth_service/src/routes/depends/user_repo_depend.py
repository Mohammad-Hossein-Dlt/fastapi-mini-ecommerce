from fastapi import Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from .db_depend import get_db_depend
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.postgresql.user_pg_repo import UserPgRepo
from src.repo.mongodb.user_mongodb_repo import UserMongodbRepo

def get_user_repo(
    db_client: AsyncIOMotorClient | Session = Depends(get_db_depend)
) -> IUserRepo:
    
    if isinstance(db_client, Session):
        return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return UserMongodbRepo()