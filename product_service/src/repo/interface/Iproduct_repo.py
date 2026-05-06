from abc import ABC, abstractmethod
from src.domain.schemas.product.product_model import ProductModel
from src.models.schemas.filter.products_filter_input import ProductFilterInput

class IProductRepo(ABC):
        
    @abstractmethod
    async def create(
        product: ProductModel,
    ) -> ProductModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        product_id: str,
    ) -> ProductModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        product: ProductModel,
    ) -> ProductModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        product_id: str,
    ) -> bool:
    
        raise NotImplementedError
        
    @abstractmethod
    async def get_by_criteria(
        criteria: ProductFilterInput,
    ) -> list[ProductModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all() -> bool:
    
        raise NotImplementedError