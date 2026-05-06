from abc import ABC, abstractmethod
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials

class IAuthService(ABC):
    
    @abstractmethod
    async def register(
        user: UserRegisterInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def login(
        user: UserLoginInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def refresh_token(
        credentials: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def admin_get_self(
        credentials: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError
        
    @abstractmethod
    async def admin_get_user(
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def admin_delete_user(
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def user_get_self(
        credentials: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def user_delete_self(
        credentials: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError