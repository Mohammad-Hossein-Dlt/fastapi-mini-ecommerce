from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.order.order_model import OrderModel
from src.domain.enums import Status
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.infra.utils.convert_id import convert_id

class OrderCollection(OrderModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: int | PydanticObjectId
    product_id: int | PydanticObjectId
    quantity: int | None = None
    description: str | None = None
    status: Status
    
    class Settings:
        name = "Orders"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
    

    @classmethod
    def create_query_by_filter(
        cls,
        filter_order: FilterOrderInput,
    ):
        
        query = {}
        

        if filter_order.user_id:
            query[str(cls.user_id)] = convert_id(filter_order.user_id)       

        if filter_order.product_id:
            query[str(cls.product_id)] = convert_id(filter_order.product_id)

        if filter_order.statuses:
            query[str(cls.status)] = {"$in": filter_order.statuses}

        if filter_order.start_quantity:
            query[str(cls.quantity)] = {"$gte": filter_order.start_quantity}

        if filter_order.end_quantity:
            query.setdefault(str(cls.quantity), {})
            query[str(cls.quantity)]["$lte"] = filter_order.end_quantity
        
        if filter_order.start_date:
            query[str(cls.created_at)] = {"$gte": filter_order.start_date}

        if filter_order.end_date:
            query.setdefault(str(cls.created_at), {})
            query[str(cls.created_at)]["$lte"] = filter_order.end_date
                    
        return query
