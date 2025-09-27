from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from datetime import datetime, timezone

class CategoryDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "categories"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)
    name = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
