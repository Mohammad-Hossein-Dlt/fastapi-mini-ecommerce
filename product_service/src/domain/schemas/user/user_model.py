from pydantic import BaseModel, model_validator
from beanie import PydanticObjectId
from datetime import datetime
from typing import Self
from src.infra.utils.convert_id import convert_id

class UserModel(BaseModel):
    
    token: str | None = None
    
    id: int | PydanticObjectId | None = None
    role: str | None = None
    name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    created_at: datetime | None = None
    
    def __setattr__(self, name, value):
        if name in ["id"]:
            value = convert_id(value)
            
        if name in ["name", "email", "username", "password", "role"]:
            value = value.strip()
        
        super().__setattr__(name, value)
        
    @model_validator(mode='after')
    def modify(
        self
    ) -> Self:
        self.id = convert_id(self.id)
        
        self.role = self.role.strip() if self.role else self.role
        self.name = self.name.strip() if self.name else self.name
        self.email = self.email.strip() if self.email else self.email
        self.username = self.username.strip() if self.username else self.username
        self.password = self.password.strip() if self.password else self.password
              
        return self