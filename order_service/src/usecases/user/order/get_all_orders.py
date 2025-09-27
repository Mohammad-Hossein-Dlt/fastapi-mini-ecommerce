from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.models.schemas.filter.filter_order_input import FilterOrderInput, UserFilterOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllOrders:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        user_id: str,
        filter_order: UserFilterOrderInput,
    ) -> list[OrderModel]:
        
        try:
            filter_order: FilterOrderInput = FilterOrderInput.model_validate(filter_order, from_attributes=True)
            filter_order.user_id = user_id
            orders: list[OrderModel] = await self.order_repo.get_all_orders(filter_order)
            return orders
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  