from abc import ABC, abstractmethod

class IAuthService(ABC):
    
    @abstractmethod
    async def admin_get_self(
        access_token: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def user_get_self(
        access_token: str,
    ) -> dict:
        
        raise NotImplementedError