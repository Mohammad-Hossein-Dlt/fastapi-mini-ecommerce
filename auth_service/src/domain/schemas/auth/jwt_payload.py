from src.infra.utils.custom_base_model import CustomBaseModel
from typing import Literal
from datetime import datetime

class JWTPayload(CustomBaseModel):
    user_id: str
    type: Literal["access", "refresh"]
    exp: datetime | None = None