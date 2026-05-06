from src.gateway.internal.interface.Iorder_service import IOrderService
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
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
        criteria: FilterOrderInput,
    ) -> list[OrderModel]:
        
        try:
            response: dict = await self.order_service.get_by_criteria(credentials, criteria)
            return [ OrderModel.model_validate(order) for order in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  