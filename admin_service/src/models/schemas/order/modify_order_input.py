from pydantic import BaseModel
from src.domain.enums import Status

class ModifyOrderInput(BaseModel):
    id: str
    status: Status | None = None
