from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field, field_serializer
from beanie import PydanticObjectId
from datetime import datetime
from src.domain.schemas.category.category_model import CategoryModel

class ProductModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    category_id: int | PydanticObjectId | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: float | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    related_categories: list[CategoryModel] = Field(default=[])
    
    @field_serializer("related_categories", return_type=list[dict])
    def category_validator(self, value: list[CategoryModel]):
        return [ category.model_dump(include={"id", "parent_id", "name"}) for category in value ]
    
