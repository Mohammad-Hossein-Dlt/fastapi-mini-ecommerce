from pydantic import BaseModel, ConfigDict
from beanie import PydanticObjectId
from datetime import datetime
from src.domain.enums import Status

class OrderModel(BaseModel):
    id: int | PydanticObjectId | None = None
    user_id: int | PydanticObjectId | None = None
    product_id: int | PydanticObjectId | None = None
    quantity: int | None = None
    description: str | None = None
    status: Status | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    model_config = ConfigDict(
        extra='allow',
    )