from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.infra.external_api.interface.Iproduct_service import IProductService
from src.domain.schemas.product.product_model import ProductModel
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.domain.schemas.order.order_model import OrderModel
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
        access_token: str,
        order: PlaceOrderInput,
        user_id: str,
    ) -> OrderModel:
        
        try:
            product = self.product_service.get_product(access_token, order.product_id)
            product: ProductModel = ProductModel.model_validate(product)
        except AppBaseException:
            raise
        
        try:
            order: OrderModel = OrderModel.model_validate(order, from_attributes=True)
            order.product_id = product.id
            order.user_id = user_id
            order.status = Status.pending
            
            if not order.quantity or order.quantity < 1:
                raise InvalidRequestException(400, "Quantity must be at least 1")
            
            return await self.order_repo.place_order(order)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  