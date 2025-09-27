from abc import ABC, abstractmethod
from src.domain.schemas.product.product_model import ProductModel
from src.models.schemas.filter.products_filter_input import ProductFilterInput
class IProductRepo(ABC):
        
    @abstractmethod
    async def insert_product(
        product: ProductModel,
    ) -> ProductModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_products(
        product_filter: ProductFilterInput,
    ) ->  list[ProductModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_product_by_id(
        product_id: str,
    ) ->  ProductModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_product(
        product: ProductModel,
    ) ->  ProductModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_products() -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_product(
        product_id: str,
    ) -> bool:
    
        raise NotImplementedError