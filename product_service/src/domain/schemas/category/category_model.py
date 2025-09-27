from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime, timezone
from typing import Self

class CategoryModel(BaseModel):
    
    id: int | None = None
    parent_id: int | None = None
    name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        extra='allow',
    )
    
    def __setattr__(self, name, value):
        now: datetime = datetime.now(timezone.utc)
        super().__setattr__(name, value)
        super().__setattr__("updated_at", now)
        
    @model_validator(mode='after')
    def set_updated_at(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = datetime.now(timezone.utc)
        return self