from pydantic import BaseModel

class CreateProductInput(BaseModel):
    category_id: int | str
    name: str
    description: str | None = None
    price: float | None = None
    stock: float | None = None