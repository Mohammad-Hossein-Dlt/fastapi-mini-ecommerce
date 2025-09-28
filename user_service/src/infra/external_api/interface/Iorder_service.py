from abc import ABC, abstractmethod
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.filter_order_input import UserFilterOrderInput
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.models.schemas.order.update_order_input import UpdateOrderInput

class IOrderService(ABC):
    
    @abstractmethod
    def user_place_order(
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def user_get_one(
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def user_get_all(
        credentials: AuthCredentials,
        order_filter: UserFilterOrderInput,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def user_update_one(
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
        
        raise NotImplementedError