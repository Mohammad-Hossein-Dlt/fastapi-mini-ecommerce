from pydantic import BaseModel
from src.domain.enums import Role

class CreateUserInput(BaseModel):
    role: Role = Role.user    
    name: str
    email: str
    username: str
    password: str
