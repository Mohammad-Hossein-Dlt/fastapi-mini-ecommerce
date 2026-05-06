from pydantic import BaseModel
from src.domain.enums import Status
from datetime import datetime

class FilterOrderInput(BaseModel):
    user_id: int | str | None = None
    product_id: int | str | None = None
    status: list[Status] | None = None
    start_quantity: int | None = None
    end_quantity: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None