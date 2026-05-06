from abc import ABC, abstractmethod
from src.domain.schemas.order.order_model import OrderModel
from src.models.schemas.filter.order_filter_input import OrderFilterInput

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
        criteria: OrderFilterInput,
    ) -> list[OrderModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_criteria(
        criteria: OrderFilterInput,
    ) -> bool:
    
        raise NotImplementedError