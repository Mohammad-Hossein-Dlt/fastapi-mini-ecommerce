from pydantic import BaseModel
from src.dto.enums import Status

class ModifyOrderInput(BaseModel):
    id: int | str
    status: Status | None = None
