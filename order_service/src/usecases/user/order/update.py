from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.dto.schemas.user.user_model import UserModel
from src.schemas.order.update_order_input import UpdateOrderInput
from src.dto.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, InvalidRequestException, OperationFailureException

class UpdateOrder:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        user: UserModel,
        entity: UpdateOrderInput,
    ) -> OrderModel:
        
        try:
            order_model: OrderModel = OrderModel.model_validate(entity, from_attributes=True)
            if order_model.quantity is not None and order_model.quantity < 1:
                raise InvalidRequestException(400, "Quantity must be at least 1")
            order_model.user_id = user.id
            return await self.order_repo.update(order_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")