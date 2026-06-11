from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text, Enum, select
from sqlalchemy.sql import Select
from src.dto.enums import Status
from datetime import datetime, timezone
from src.schemas.filter.order_filter_input import OrderFilterInput

class OrderDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "Order"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Text, nullable=False)
    product_id = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
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
        criteria: OrderFilterInput,
    ) -> Select["OrderDBModel"]:
        
        query = select(cls)
        
        if criteria.user_id:
            query = query.where(
                cls.user_id == str(criteria.user_id)
            )        
            
        if criteria.product_id:
            query = query.where(
                cls.product_id == str(criteria.product_id)
            )
        
        if criteria.status:
            query = query.where(
                cls.status.in_(
                    criteria.status,   
                )
            )
        
        if criteria.start_quantity:
            query = query.where(
                cls.quantity >= criteria.start_quantity
            )
        
        
        if criteria.end_quantity:
            query = query.where(
                cls.quantity <= criteria.end_quantity
            )
        
        if criteria.start_date:
            query = query.where(
                cls.created_at >= criteria.start_date
            )
        
        if criteria.end_date:
            query = query.where(
                cls.created_at <= criteria.end_date
            )
        
        return query

