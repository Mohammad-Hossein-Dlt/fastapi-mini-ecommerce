from abc import ABC, abstractmethod

class IProductService(ABC):
    
    @abstractmethod
    def get_product(
        access_token: str,
        product_id: str,
    ) -> dict:
        
        raise NotImplementedError