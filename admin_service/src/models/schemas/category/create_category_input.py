from pydantic import BaseModel

class CreateCategoryInput(BaseModel):
    parent_id: int | str | None = None
    name: str

