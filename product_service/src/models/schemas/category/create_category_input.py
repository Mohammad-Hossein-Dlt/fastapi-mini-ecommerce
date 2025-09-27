from pydantic import BaseModel

class CreateCategoryInput(BaseModel):
    parent_id: int | None = None
    name: str

