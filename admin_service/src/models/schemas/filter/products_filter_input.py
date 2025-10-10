from pydantic import BaseModel

class ProductFilterInput(BaseModel):
    category_id: int | str | None = None
    start_price: float | None = None
    end_price: float | None = None
