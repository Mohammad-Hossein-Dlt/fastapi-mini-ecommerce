from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, Float, select
from sqlalchemy.sql import Select
from datetime import datetime, timezone
from src.models.schemas.filter.product_filter_input import ProductFilterInput

class ProductDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "Product"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    category_id = Column(Integer, ForeignKey("Category.id"), nullable=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    @classmethod
    def create_filter_query(
        cls,
        criteria: ProductFilterInput,
    ) -> Select["ProductDBModel"]:
        
        query = select(cls)
        
        if criteria.category_id:
            query = query.where(
                cls.category_id == int(criteria.category_id)
            )
        
        if criteria.start_price:
            query = query.where(
                cls.price >= criteria.start_price
            )
        
        if criteria.end_price:
            query = query.where(
                cls.price <= criteria.end_price
            )
        
        return query

