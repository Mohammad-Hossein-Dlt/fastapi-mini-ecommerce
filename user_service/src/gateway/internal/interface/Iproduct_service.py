from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.product_filter_input import ProductFilterInput

class IProductService(ABC):
        
    @abstractmethod
    async def get_by_id(
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