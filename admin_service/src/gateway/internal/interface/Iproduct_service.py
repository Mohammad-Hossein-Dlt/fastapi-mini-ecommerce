from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.product.create_product_input import CreateProductInput
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.models.schemas.filter.product_filter_input import ProductFilterInput

class IProductService(ABC):
    
    @abstractmethod
    async def create(
        credentials: AuthCredentials,
        product: CreateProductInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        raise NotImplementedError        
    
    @abstractmethod
    async def update(
        credentials: AuthCredentials,
        product: UpdateProductInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        credentials: AuthCredentials,
        criteria: ProductFilterInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all(
        credentials: AuthCredentials,
    ) -> dict:
    
        raise NotImplementedError