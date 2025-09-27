from pydantic import BaseModel

class UpdateCategoryInput(BaseModel):
    id: int
    parent_id: int | None = None
    name: str | None = None