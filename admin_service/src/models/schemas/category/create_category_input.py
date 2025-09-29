from pydantic import BaseModel

class CreateCategoryInput(BaseModel):
    parent_id: str | None = None
    name: str

