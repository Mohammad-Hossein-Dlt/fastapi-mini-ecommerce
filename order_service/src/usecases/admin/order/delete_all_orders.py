from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminDeleteAllOrders:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo   
    
    async def execute(
        self,
        filter_order: FilterOrderInput,
    ) -> OperationOutput:
        
        try:
            status = await self.order_repo.delete_all_orders(filter_order)
            return OperationOutput(id=None, request="delete/all_orders", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  