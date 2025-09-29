from pydantic import BaseModel, model_validator, field_validator, field_serializer
from bson.objectid import ObjectId
from typing import TypeAlias, Literal, ClassVar, Any

db_stack_types: TypeAlias = Literal["no-sql", "sql"]

class CustomBaseModel(BaseModel):
    
    aliases: ClassVar[dict[str, str]] = {
        "id": "_id"
    }
    
    @model_validator(mode="before")
    def alias_validator(cls, values) -> dict:
                
        if isinstance(values, dict):
            
            for k, v in cls.aliases.items():      
                if v in values:
                    values[k] = values.pop(v)
                    
        return values
    
    @field_validator("*")
    def object_id_validator(cls, var):
        if ObjectId.is_valid(var):
            return ObjectId(var)
        return var
    
    @field_serializer("*")
    def object_id_serializer(self, var):
        if ObjectId.is_valid(var):
            return str(var)
        return var

    def custom_model_dump(
        self,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        exclude: set = None,
        db_stack: db_stack_types = "no-sql",
    ) -> dict[str, Any]:
        
        dumped = self.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude=exclude,
            mode="python",
        )

        if db_stack == "no-sql": 
            for key, value in self.aliases.items():
                if key in dumped:
                    dumped[value] = dumped.pop(key)
                
        return dumped