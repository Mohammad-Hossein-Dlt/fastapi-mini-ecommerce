from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.dto.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrders:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        criteria: OrderFilterInput,
    ) -> list[OrderModel]:
        
        try:
            return await self.order_repo.get_by_criteria(criteria)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  