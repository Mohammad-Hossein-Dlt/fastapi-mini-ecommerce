from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.dto.schemas.user.user_model import UserModel
from src.dto.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrder:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        user: UserModel,
        order_id: str,
    ) -> OrderModel:
        
        try:
            return await self.order_repo.get_by_id_and_user_id(order_id, user.id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")