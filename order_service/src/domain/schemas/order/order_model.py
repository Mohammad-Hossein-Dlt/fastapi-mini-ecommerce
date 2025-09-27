from pydantic import BaseModel, Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from src.domain.enums import Status
from src.infra.utils.convert_id import convert_id
from typing import Self

class OrderModel(BaseModel):
    id: int | PydanticObjectId | None = None
    user_id: int | PydanticObjectId | None = None
    product_id: int | PydanticObjectId | None = None
    quantity: int | None = None
    description: str | None = None
    status: Status | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __setattr__(self, name, value):
        if self.updated_at is None:
            now: datetime = datetime.now(timezone.utc)
            super().__setattr__("updated_at", now)
        
        if name in ["id", "user_id", "product_id"]:
            value = convert_id(value)
        
        super().__setattr__(name, value)
        
    @model_validator(mode='after')
    def set_updated_at(
        self
    ) -> Self:
        if "updated_at" not in self.model_fields_set:
            self.updated_at = datetime.now(timezone.utc)
        
        self.id = convert_id(self.id)
        self.user_id = convert_id(self.user_id)
        self.product_id = convert_id(self.product_id)
        
        return self