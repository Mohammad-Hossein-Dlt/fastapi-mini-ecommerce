from pydantic import BaseModel
from src.domain.enums import Status

class ModifyOrderInput(BaseModel):
    id: int | str
    status: Status | None = None
