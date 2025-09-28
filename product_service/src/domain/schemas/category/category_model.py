from pydantic import BaseModel, ConfigDict, Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from src.infra.utils.convert_id import convert_id
from typing import ClassVar, Self, Any

class CategoryModel(BaseModel):
    
    id: int | PydanticObjectId | None = None
    parent_id: int | PydanticObjectId | None = None
    name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    aliases: ClassVar[dict[str, str]] = {
        "id": "_id"
    }
    
    exclude_if_none: ClassVar[list[str]] = [
        "name",
    ]
    
    model_config = ConfigDict(
        extra='allow',
    )
    
    def __setattr__(
        self,
        name,
        value,
    ):
        if name in ["id", "parent_id"]:
            value = convert_id(value)
        elif name in ["name"] and isinstance(value, str):
            value = value.strip()
        elif self.updated_at is None:
            value: datetime = datetime.now(timezone.utc)
            super().__setattr__("updated_at", value)
            
        super().__setattr__(name, value)
        
    @model_validator(mode='after')
    def set_updated_at(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = datetime.now(timezone.utc)
        
        self.id = convert_id(self.id)
        self.parent_id = convert_id(self.parent_id)
        self.name = self.name.strip() if self.name else self.name
        
        return self
    
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:
        
        for k, v in cls.aliases.items():            
            if v in values:
                values[k] = values.pop(v)
        return values
    
    def model_dump_to_update(
        self,
        include = None,
        exclude = None,
        by_alias = None,
        exclude_unset = False,
        exclude_defaults = False,
        exclude_none = False,
    ) -> dict[str, Any]:
        
        dumped = self.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            mode="python",
        )
        
        for key, value in self.aliases.items():
            if key in dumped:
                dumped[value] = dumped.pop(key)
        
        for value in self.exclude_if_none:
            if value in dumped and dumped.get(value) is None:
                dumped.pop(value)
        
        return dumped