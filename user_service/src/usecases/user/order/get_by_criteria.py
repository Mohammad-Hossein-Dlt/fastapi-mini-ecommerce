from src.gateway.internal.interface.Iorder_service import IOrderService
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.dto.schemas.order.order_model import OrderModel
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrders:
    
    def __init__(
        self,
        order_service: IOrderService,
    ):        
        self.order_service = order_service  
    
    async def execute(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list[OrderModel]:
        
        try:
            response: dict = await self.order_service.get_by_criteria(credentials, criteria)
            return [ OrderModel.model_validate(order) for order in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  