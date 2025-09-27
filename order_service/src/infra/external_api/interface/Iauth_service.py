from abc import ABC, abstractmethod

class IAuthService(ABC):
    
    @abstractmethod
    def admin_get_self(
        access_token: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def admin_get_user(
        access_token: str,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:

        raise NotImplementedError
    
    @abstractmethod
    def user_get_self(
        access_token: str,
    ) -> dict:
        
        raise NotImplementedError