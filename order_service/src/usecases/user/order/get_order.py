from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrder:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        order_id: str,
        user_id: str,
    ) -> OrderModel:
        
        try:
            return await self.order_repo.get_order_by_id(order_id, user_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")