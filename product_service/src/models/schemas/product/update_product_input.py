from pydantic import BaseModel

class UpdateProductInput(BaseModel):
    id: int | str
    category_id: int | str | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: float | None = None