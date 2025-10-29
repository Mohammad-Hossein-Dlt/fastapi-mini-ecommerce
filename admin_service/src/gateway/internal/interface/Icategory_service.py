from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput

class ICategoryService(ABC):
    
    @abstractmethod
    async def create(
        credentials: AuthCredentials,
        category_data: CreateCategoryInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all(
        credentials: AuthCredentials,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one(
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
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
    
    @abstractmethod
    async def update_one(
        credentials: AuthCredentials,
        category_data: UpdateCategoryInput,
    ) -> dict:
        
        raise NotImplementedError