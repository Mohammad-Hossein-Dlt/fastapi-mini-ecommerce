from abc import ABC, abstractmethod
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.schemas.order.place_order_input import PlaceOrderInput
from src.schemas.order.update_order_input import UpdateOrderInput

class IOrderService(ABC):
    
    @abstractmethod
    async def place_order(
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        raise NotImplementedError