from fastapi import Depends
from .db_depend import db_depend
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from sqlalchemy import text

async def health_check(
    db: AsyncIOMotorClient | Session = Depends(db_depend)
):
    if isinstance(db, Session):
        try:
            request = db.execute(text("SELECT 1"))
            _ = request.scalar()
            return True
        except:
            db.rollback()
            return False
    
    if isinstance(db, AsyncIOMotorClient):
        try:
            await db.admin.command("ping")
            return True
        except Exception:
            return False