from pydantic import BaseModel, model_validator
from typing import Self

class CreateProductInput(BaseModel):
    category_id: int | str
    name: str
    description: str | None = None
    price: float | None = None
    stock: float | None = None

    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if not self.price:
            self.price = 0
        
        if not self.stock:
            self.stock = 0
        
        return self