from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.order.order_model import OrderModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetOrders:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
    ):        
        self.order_repo = order_repo  
    
    async def execute(
        self,
        user: UserModel,
        criteria: FilterOrderInput,
    ) -> list[OrderModel]:
        
        try:
            criteria: FilterOrderInput = FilterOrderInput.model_validate(criteria, from_attributes=True)
            criteria.user_id = user.id if user and user.id else criteria.user_id
            orders: list[OrderModel] = await self.order_repo.get_by_criteria(criteria)
            return orders
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  