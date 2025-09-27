from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime, timezone
from typing import Self

class ProductModel(BaseModel):
    id: int | None = None
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        extra='allow',
    )
    
    def __setattr__(self, name, value):
        if self.updated_at is None:
            now: datetime = datetime.now(timezone.utc)
            super().__setattr__("updated_at", now)
        
        super().__setattr__(name, value)
        
    @model_validator(mode='after')
    def set_updated_at(
        self
    ) -> Self:
        if "updated_at" not in self.model_fields_set:
            self.updated_at = datetime.now(timezone.utc)
        return self