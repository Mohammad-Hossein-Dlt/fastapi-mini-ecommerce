from pydantic import BaseModel
from src.domain.enums import Status
from datetime import datetime

class FilterOrderInput(BaseModel):
    user_id: str | None = None
    product_id: str | None = None
    statuses: list[Status] | None = None
    start_quantity: int | None = None
    end_quantity: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    
    
class UserFilterOrderInput(BaseModel):
    product_id: str | None = None
    statuses: list[Status] | None = None
    start_quantity: int | None = None 
    end_quantity: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None