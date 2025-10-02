from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field
from beanie import PydanticObjectId
from datetime import datetime, timezone
from src.domain.enums import Role

class UserModel(CustomBaseModel):
    id: int | PydanticObjectId | None = None
    role: Role | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))