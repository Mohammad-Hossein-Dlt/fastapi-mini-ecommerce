from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.products_filter_input import ProductFilterInput

class IProductService(ABC):
    
    @abstractmethod
    async def get_all(
        credentials: AuthCredentials,
        product_filter: ProductFilterInput,
    ) -> dict:
        
        raise NotImplementedError
        
    @abstractmethod
    async def get_one(
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        raise NotImplementedError