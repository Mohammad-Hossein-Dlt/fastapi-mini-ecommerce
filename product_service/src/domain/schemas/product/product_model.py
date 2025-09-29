from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import ConfigDict, Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import Self

class ProductModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    category_id: int | PydanticObjectId | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: float | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        extra='allow',
    )
        
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
            
        return self