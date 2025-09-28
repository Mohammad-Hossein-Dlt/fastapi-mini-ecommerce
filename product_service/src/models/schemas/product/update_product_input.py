from pydantic import BaseModel

class UpdateProductInput(BaseModel):
    id: str
    category_id: str | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None