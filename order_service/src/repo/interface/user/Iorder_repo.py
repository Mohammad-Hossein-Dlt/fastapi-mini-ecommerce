from abc import ABC, abstractmethod
from src.domain.schemas.order.order_model import OrderModel
from src.models.schemas.filter.order_filter_input import OrderFilterInput

class IOrderRepo(ABC):
        
    @abstractmethod
    async def create(
        order: OrderModel,
    ) -> OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        order_id: str,
    ) -> OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id_and_user_id(
        order_id: str,
        user_id: str,
    ) -> OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        order: OrderModel,
    ) -> OrderModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        order_id: str,
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_criteria(
        criteria: OrderFilterInput,
    ) -> list[OrderModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    