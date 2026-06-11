from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteOrders:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo   
    
    async def execute(
        self,
        criteria: OrderFilterInput,
    ) -> OperationOutput:
        
        try:
            status = await self.order_repo.delete_by_criteria(criteria)
            return OperationOutput(id=None, request="delete/all_orders", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  