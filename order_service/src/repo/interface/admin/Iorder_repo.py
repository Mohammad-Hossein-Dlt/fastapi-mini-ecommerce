from abc import ABC, abstractmethod
from src.domain.schemas.order.order_model import OrderModel
from src.models.schemas.filter.filter_order_input import FilterOrderInput

class IAdminOrderRepo(ABC):
        
    @abstractmethod
    async def get_all_orders(
        filter_order: FilterOrderInput,
    ) ->  list[OrderModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_order_by_id(
        order_id: str,
    ) ->  OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def modify_order(
        order: OrderModel,
    ) ->  OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_orders(
        filter_order: FilterOrderInput,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_order(
        order_id: str,
    ) -> bool:
    
        raise NotImplementedError