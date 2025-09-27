from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.models.schemas.order.modify_order import ModifyOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateOrder:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        order: ModifyOrderInput,
    ) -> OrderModel:
        
        try:
            order: OrderModel = OrderModel.model_validate(order, from_attributes=True)
            return await self.order_repo.modify_order(order)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")