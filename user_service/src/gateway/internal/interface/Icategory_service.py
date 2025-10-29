from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput

class ICategoryService(ABC):
    
    @abstractmethod
    async def get_all(
        credentials: AuthCredentials,
        category_filter: CategoryFilterInput,
    ) -> dict:
        
        raise NotImplementedError
        
    @abstractmethod
    async def get_one(
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        raise NotImplementedError