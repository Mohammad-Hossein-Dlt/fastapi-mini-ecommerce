from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, Float, select
from sqlalchemy.sql import Select
from datetime import datetime, timezone
from src.models.schemas.filter.products_filter_input import ProductFilterInput

class ProductDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "products"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    stock = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    @classmethod
    def create_filter_query(
        cls,
        product_filter: ProductFilterInput,
    ) -> Select["ProductDBModel"]:
        query = select(cls)
        
        if product_filter.category_id:
            query = query.where(
                cls.category_id == product_filter.category_id
            )
        
        if product_filter.start_price:
            query = query.where(
                cls.price >= product_filter.start_price
            )
        
        if product_filter.end_price:
            query = query.where(
                cls.price <= product_filter.end_price
            )
        
        return query

