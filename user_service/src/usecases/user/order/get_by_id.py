from src.gateway.internal.interface.Iorder_service import IOrderService
from src.dto.schemas.order.order_model import OrderModel
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrder:
    
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
            response: dict = await self.order_service.get_by_id(credentials, order_id)
            return OrderModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  