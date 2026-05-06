from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.category_filter_input import CategoryFilterInput

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
    ) -> dict:
        
        raise NotImplementedError