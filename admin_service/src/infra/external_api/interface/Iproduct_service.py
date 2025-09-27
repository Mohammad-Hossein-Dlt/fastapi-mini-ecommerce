from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.product.create_product_input import CreateProductInput
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.models.schemas.filter.products_filter_input import ProductFilterInput

class IProductService(ABC):
    
    @abstractmethod
    def create(
        credentials: AuthCredentials,
        product_data: CreateProductInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    def delete_all(
        credentials: AuthCredentials,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    def delete_one(
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def get_all(
        credentials: AuthCredentials,
        product_filter: ProductFilterInput,
    ) -> dict:
        
        raise NotImplementedError
        
    @abstractmethod
    def get_one(
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        raise NotImplementedError        
    
    @abstractmethod
    def update_one(
        credentials: AuthCredentials,
        product_data: UpdateProductInput,
    ) -> dict:
        
        raise NotImplementedError