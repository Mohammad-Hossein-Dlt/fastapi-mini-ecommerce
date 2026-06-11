from pydantic import BaseModel

class UpdateOrderInput(BaseModel):
    id: int | str
    description: str | None = None