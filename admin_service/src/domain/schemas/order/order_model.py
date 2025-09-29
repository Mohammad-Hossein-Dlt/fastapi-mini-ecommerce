from src.infra.utils.custom_base_model import CustomBaseModel
from beanie import PydanticObjectId
from datetime import datetime

class OrderModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    user_id: int | PydanticObjectId | None = None
    product_id: int | PydanticObjectId | None = None
    quantity: int | None = None
    description: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
