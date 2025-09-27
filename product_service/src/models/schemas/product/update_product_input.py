from pydantic import BaseModel

class UpdateProductInput(BaseModel):
    id: int
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None