from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import user_order_repo_depend
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.worker.depends.internal_http_depend import product_service_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.user.order.place_order import PlaceOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.user.place-order"

@client.broker.subscriber(
    subject=routing_key,
)
async def place_order(
    entity: PlaceOrderInput,
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    product_service: IProductService = Depends(product_service_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_order_usecase = PlaceOrder(order_repo, product_service)
        output = await get_order_usecase.execute(user, entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
