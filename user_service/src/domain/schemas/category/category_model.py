from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field
from beanie import PydanticObjectId
from datetime import datetime
from typing import Self

class CategoryModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    parent_id: int | PydanticObjectId | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    children: list[Self] = Field(default=[])
    
