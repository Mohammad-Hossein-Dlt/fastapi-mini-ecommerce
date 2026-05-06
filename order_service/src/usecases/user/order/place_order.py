from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.domain.schemas.order.order_model import OrderModel
from src.domain.schemas.product.product_model import ProductModel
from src.domain.enums import Status
from src.infra.exceptions.exceptions import AppBaseException, InvalidRequestException, OperationFailureException

class PlaceOrder:
    
    def __init__(
        self,
        order_repo: IOrderRepo,
        product_service: IProductService,
    ):        
        self.order_repo = order_repo
        self.product_service = product_service
    
    async def execute(
        self,
        user: UserModel,
        entity: PlaceOrderInput,
    ) -> OrderModel:
                
        try:
            product = await self.product_service.get_by_id(user.token, entity.product_id)
            product: ProductModel = ProductModel.model_validate(product)
            
            order_model: OrderModel = OrderModel.model_validate(entity, from_attributes=True)
            order_model.user_id = user.id
            order_model.product_id = product.id
            order_model.status = Status.PENDING

            if not order_model.quantity or order_model.quantity < 1:
                raise InvalidRequestException(400, "Quantity must be at least 1")
            
            return await self.order_repo.create(order_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  