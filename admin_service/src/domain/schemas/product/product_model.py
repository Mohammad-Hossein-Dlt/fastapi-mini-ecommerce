from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProductModel(BaseModel):
    id: int | None = None
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    model_config = ConfigDict(
        extra='allow',
    )