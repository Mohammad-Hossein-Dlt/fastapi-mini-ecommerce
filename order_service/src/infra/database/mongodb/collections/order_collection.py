from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import Field
from src.domain.schemas.order.order_model import OrderModel
from src.domain.enums import Status
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.infra.utils.convert_id import convert_database_id

class OrderCollection(OrderModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: int | PydanticObjectId
    product_id: int | PydanticObjectId
    quantity: int = 0
    description: str | None = None
    status: Status
    
    class Settings:
        name = "Order"

    @classmethod
    def create_filter_query(
        cls,
        criteria: FilterOrderInput,
    ):
        
        query = {}
        

        if criteria.user_id:
            query[str(cls.user_id)] = convert_database_id(criteria.user_id)       

        if criteria.product_id:
            query[str(cls.product_id)] = convert_database_id(criteria.product_id)

        if criteria.status:
            query[str(cls.status)] = {"$in": criteria.status}

        if criteria.start_quantity:
            query[str(cls.quantity)] = {"$gte": criteria.start_quantity}

        if criteria.end_quantity:
            query.setdefault(str(cls.quantity), {})
            query[str(cls.quantity)]["$lte"] = criteria.end_quantity
        
        if criteria.start_date:
            query[str(cls.created_at)] = {"$gte": criteria.start_date}

        if criteria.end_date:
            query.setdefault(str(cls.created_at), {})
            query[str(cls.created_at)]["$lte"] = criteria.end_date
                    
        return query
