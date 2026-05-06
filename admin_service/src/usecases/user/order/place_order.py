from src.gateway.internal.interface.Iorder_service import IOrderService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class PlaceOrder:
    
    def __init__(
        self,
        order_service: IOrderService,
    ):        
        self.order_service = order_service 
    
    async def execute(
        self,
        credentials: AuthCredentials,
        entity: PlaceOrderInput,
    ) -> OrderModel:
        
        try:
            response: dict = await self.order_service.place_order(credentials, entity)
            return OrderModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  