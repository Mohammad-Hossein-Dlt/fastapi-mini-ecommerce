from src.infra.external_api.interface.Iorder_service import IOrderService
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminGetAllOrders:
    
    def __init__(
        self,
        order_service: IOrderService,
    ):        
        self.order_service = order_service  
    
    async def execute(
        self,
        credentials: AuthCredentials,
        order_filter: FilterOrderInput,
    ) -> list[OrderModel]:
        
        try:
            response: dict = self.order_service.admin_get_all(credentials, order_filter)
            return [ OrderModel.model_validate(order) for order in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  