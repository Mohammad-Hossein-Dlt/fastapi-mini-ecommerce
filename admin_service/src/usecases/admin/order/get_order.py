from src.infra.external_api.interface.Iorder_service import IOrderService
from src.domain.schemas.order.order_model import OrderModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminGetOrder:
    
    def __init__(
        self,
        order_service: IOrderService,
    ):        
        self.order_service = order_service 
    
    async def execute(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> OrderModel:
        
        try:
            response: dict = self.order_service.admin_get_one(credentials, order_id)
            return OrderModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  