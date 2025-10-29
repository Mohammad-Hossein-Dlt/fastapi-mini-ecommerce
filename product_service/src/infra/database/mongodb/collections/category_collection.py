from src.domain.schemas.category.category_model import CategoryModel
from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import Field
from datetime import datetime, timezone

class CategoryCollection(CategoryModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    parent_id: PydanticObjectId | None = None
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "Categories"