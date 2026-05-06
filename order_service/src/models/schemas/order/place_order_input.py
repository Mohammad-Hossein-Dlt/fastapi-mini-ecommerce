from pydantic import BaseModel, model_validator
from typing import Self

class PlaceOrderInput(BaseModel):
    product_id: int | str
    quantity: int | None = None
    description: str | None = None

    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if not self.quantity:
            self.quantity = 0
                
        return self
