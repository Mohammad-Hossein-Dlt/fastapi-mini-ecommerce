from abc import ABC, abstractmethod
from src.domain.schemas.order.order_model import OrderModel
from src.models.schemas.filter.filter_order_input import FilterOrderInput

class IOrderRepo(ABC):
        
    @abstractmethod
    async def place_order(
        order: OrderModel,
    ) -> OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_orders(
        filter_order: FilterOrderInput,
    ) ->  list[OrderModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_order_by_id(
        order_id: str,
        user_id: str,
    ) ->  OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def check_order(
        user_id: str,
        product_id: str,
    ) ->  OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_order(
        order: OrderModel,
    ) ->  OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_orders(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_order(
        order_id: str,
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError