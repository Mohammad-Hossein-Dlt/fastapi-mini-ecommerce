from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.models.schemas.filter.category_filter_input import CategoryFilterInput

class ICategoryService(ABC):
    
    @abstractmethod
    async def create(
        credentials: AuthCredentials,
        category: CreateCategoryInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        raise NotImplementedError        
    
    @abstractmethod
    async def update(
        credentials: AuthCredentials,
        category: UpdateCategoryInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
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

    @abstractmethod
    async def delete_all(
        credentials: AuthCredentials,
    ) -> dict:
    
        raise NotImplementedError
        