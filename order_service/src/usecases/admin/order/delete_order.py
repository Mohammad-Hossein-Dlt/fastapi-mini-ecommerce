from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminDeleteOrder:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo   
    
    async def execute(
        self,
        order_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.order_repo.delete_order(order_id)
            return OperationOutput(id=order_id, request="delete/order", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  