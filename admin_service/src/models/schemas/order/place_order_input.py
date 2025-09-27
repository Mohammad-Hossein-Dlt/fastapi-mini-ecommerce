from pydantic import BaseModel

class PlaceOrderInput(BaseModel):
    product_id: str
    quantity: int | None = None
    description: str | None = None
