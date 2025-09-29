from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from src.domain.enums import Status
from typing import Self

class OrderModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    user_id: int | PydanticObjectId | None = None
    product_id: int | PydanticObjectId | None = None
    quantity: int | None = None
    description: str | None = None
    status: Status | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self