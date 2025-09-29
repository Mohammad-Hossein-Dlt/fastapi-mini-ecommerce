from pydantic import BaseModel

class UpdateCategoryInput(BaseModel):
    id: str
    parent_id: str | None = None
    name: str | None = None