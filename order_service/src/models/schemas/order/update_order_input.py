from pydantic import BaseModel

class UpdateOrderInput(BaseModel):
    id: str
    description: str | None = None