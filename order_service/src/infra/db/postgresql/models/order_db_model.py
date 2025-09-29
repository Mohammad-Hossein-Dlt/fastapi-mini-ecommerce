from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text, Enum, select
from sqlalchemy.sql import Select
from src.domain.enums import Status
from datetime import datetime, timezone
from src.models.schemas.filter.filter_order_input import FilterOrderInput

class OrderDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "orders"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Text, nullable=False)
    product_id = Column(Text, nullable=False)
    
    quantity = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    
    status = Column(Enum(Status), nullable=False)
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    def __setattr__(
        self,
        name,
        value,
    ):
        
        if name in ["user_id", "product_id"]:
            value = str(value)
                    
        super().__setattr__(name, value)
    
    @classmethod
    def create_filter_query(
        cls,
        order_filter: FilterOrderInput,
    ) -> Select["OrderDBModel"]:
        query = select(cls)
        
        if order_filter.user_id:
            query = query.where(
                cls.user_id == str(order_filter.user_id)
            )        
            
        if order_filter.product_id:
            query = query.where(
                cls.product_id == str(order_filter.product_id)
            )
        
        if order_filter.statuses:
            query = query.where(
                cls.status.in_(
                    order_filter.statuses,   
                )
            )
        
        if order_filter.start_quantity:
            query = query.where(
                cls.quantity >= order_filter.start_quantity
            )
        
        
        if order_filter.end_quantity:
            query = query.where(
                cls.quantity <= order_filter.end_quantity
            )
        
        if order_filter.start_date:
            query = query.where(
                cls.created_at >= order_filter.start_date
            )
        
        if order_filter.end_date:
            query = query.where(
                cls.created_at <= order_filter.end_date
            )
        
        return query

