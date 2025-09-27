from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllOrders:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        filter_order: FilterOrderInput,
    ) -> list[OrderModel]:
        
        try:
            orders: list[OrderModel] = await self.order_repo.get_all_orders(filter_order)
            return orders
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  