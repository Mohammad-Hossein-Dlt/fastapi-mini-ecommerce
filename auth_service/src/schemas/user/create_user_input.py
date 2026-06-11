from pydantic import BaseModel
from src.dto.enums import Role

class CreateUserInput(BaseModel):
    role: Role = Role.USER    
    name: str
    email: str
    username: str
    password: str
