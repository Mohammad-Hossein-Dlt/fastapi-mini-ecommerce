from abc import ABC, abstractmethod

class IAuthService(ABC):
    
    @abstractmethod
    async def get_admin(
        access_token: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_user(
        access_token: str,
    ) -> dict:
        
        raise NotImplementedError