from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field
from beanie import PydanticObjectId
from datetime import datetime

class UserModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    role: str | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    
    token: str | None = Field(default=None, exclude=True)
    
