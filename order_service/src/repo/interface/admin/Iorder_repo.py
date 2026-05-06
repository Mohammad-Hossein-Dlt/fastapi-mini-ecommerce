from abc import ABC, abstractmethod
from src.domain.schemas.order.order_model import OrderModel
from src.models.schemas.filter.filter_order_input import FilterOrderInput

class IAdminOrderRepo(ABC):
    
    @abstractmethod
    async def get_by_id(
        order_id: str,
    ) -> OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def modify(
        order: OrderModel,
    ) -> OrderModel:
    
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(
        order_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        criteria: FilterOrderInput,
    ) -> list[OrderModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_criteria(
        criteria: FilterOrderInput,
    ) -> bool:
    
        raise NotImplementedError