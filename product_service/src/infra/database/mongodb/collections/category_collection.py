from src.domain.schemas.category.category_model import CategoryModel
from beanie import Document, PydanticObjectId, before_event, Update
from bson import ObjectId
from pydantic import Field
from datetime import datetime, timezone

class CategoryCollection(CategoryModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    parent_id: PydanticObjectId | None = None
    name: str
    slug: str
    
    class Settings:
        name = "Category"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)