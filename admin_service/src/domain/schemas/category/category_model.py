from src.infra.utils.custom_base_model import CustomBaseModel
from beanie import PydanticObjectId
from datetime import datetime

class CategoryModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    parent_id: int | PydanticObjectId | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
