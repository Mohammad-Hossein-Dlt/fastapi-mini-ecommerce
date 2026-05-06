from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrders:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        criteria: FilterOrderInput,
    ) -> list[OrderModel]:
        
        try:
            orders: list[OrderModel] = await self.order_repo.get_by_criteria(criteria)
            return orders
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  