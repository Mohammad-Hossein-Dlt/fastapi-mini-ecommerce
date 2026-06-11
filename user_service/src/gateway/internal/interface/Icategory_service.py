from abc import ABC, abstractmethod
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.filter.category_filter_input import CategoryFilterInput

class ICategoryService(ABC):
        
    @abstractmethod
    async def get_by_id(
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        credentials: AuthCredentials,
        criteria: CategoryFilterInput,
    ) -> list:
        
        raise NotImplementedError