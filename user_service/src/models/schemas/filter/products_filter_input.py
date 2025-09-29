from pydantic import BaseModel

class ProductFilterInput(BaseModel):
    category_id: str | None = None
    start_price: float | None = None
    end_price: float | None = None
