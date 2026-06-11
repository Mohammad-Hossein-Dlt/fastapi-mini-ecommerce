from pydantic import BaseModel

class PlaceOrderInput(BaseModel):
    product_id: int | str
    quantity: int | None = None
    description: str | None = None
