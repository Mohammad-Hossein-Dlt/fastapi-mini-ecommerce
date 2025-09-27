from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CategoryModel(BaseModel):
    id: int | None = None
    parent_id: int | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    model_config = ConfigDict(
        extra='allow',
    )