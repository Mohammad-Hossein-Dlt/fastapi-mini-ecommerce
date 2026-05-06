from src.gateway.internal.interface.Iorder_service import IOrderService
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteOrders:
    
    def __init__(
        self,
        order_service: IOrderService,
    ):        
        self.order_service = order_service 
    
    async def execute(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> OperationOutput:
        
        try:
            response: dict = await self.order_service.delete_by_criteria(credentials, criteria)
            return OperationOutput.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  