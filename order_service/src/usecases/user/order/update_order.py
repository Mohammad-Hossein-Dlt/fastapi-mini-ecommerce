from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.models.schemas.order.update_order_input import UpdateOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, InvalidRequestException, OperationFailureException

class UpdateOrder:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        user_id: str,
        order: UpdateOrderInput,
    ) -> OrderModel:
        
        try:
            order: OrderModel = OrderModel.model_validate(order, from_attributes=True)
            order.user_id = user_id
            
            if (order.quantity is not None) and order.quantity < 1:
                raise InvalidRequestException(400, "Quantity must be at least 1")
            
            return await self.order_repo.update_order(order)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")