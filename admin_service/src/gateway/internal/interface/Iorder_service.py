from abc import ABC, abstractmethod
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.order.modify_order_input import ModifyOrderInput
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.schemas.order.place_order_input import PlaceOrderInput
from src.schemas.order.update_order_input import UpdateOrderInput

class IOrderService(ABC):
    
    @abstractmethod
    async def get_by_id(
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    async def modify(
        credentials: AuthCredentials,
        modify: ModifyOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_criteria(
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def place_order(
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def user_get_by_id(
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def user_update(
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    async def user_get_by_criteria(
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        raise NotImplementedError