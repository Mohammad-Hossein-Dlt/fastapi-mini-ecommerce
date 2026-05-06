from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.models.schemas.order.modify_order_input import ModifyOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ModifyOrder:
    
    def __init__(
        self,
        order_repo: IAdminOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        entity: ModifyOrderInput,
    ) -> OrderModel:
        
        try:
            order_model: OrderModel = OrderModel.model_validate(entity, from_attributes=True)
            return await self.order_repo.modify(order_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")