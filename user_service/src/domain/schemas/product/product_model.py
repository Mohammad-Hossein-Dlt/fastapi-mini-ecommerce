from src.infra.utils.custom_base_model import CustomBaseModel
from beanie import PydanticObjectId
from datetime import datetime

class ProductModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    category_id: int | PydanticObjectId | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: float | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
