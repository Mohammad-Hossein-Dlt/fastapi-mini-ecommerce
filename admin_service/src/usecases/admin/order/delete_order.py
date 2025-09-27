from src.infra.external_api.interface.Iorder_service import IOrderService
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminDeleteOrder:
    
    def __init__(
        self,
        order_service: IOrderService,
    ):        
        self.order_service = order_service   
    
    async def execute(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> OperationOutput:
        
        try:
            response: dict = self.order_service.admin_delete_one(credentials, order_id)
            return OperationOutput.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  