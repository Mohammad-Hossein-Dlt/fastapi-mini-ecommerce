from src.infra.utils.custom_base_model import CustomBaseModel
from beanie import PydanticObjectId
from datetime import datetime

from src.domain.schemas.auth.auth_credentials import AuthCredentials
from pydantic import Field

class UserModel(CustomBaseModel):
        
    id: int | PydanticObjectId | None = None
    role: str | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    
    credentials: AuthCredentials | None = Field(default=None, exclude=True)
    
