from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.worker.consumer.rabbitmq.broker import subscriber
from src.worker.depends.rabbitmq_depend import target_routing_key
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import user_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.user.order.get_by_criteria import GetOrders
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.user.get.by-criteria"

@subscriber(
    filter=target_routing_key(routing_key),
)
async def get_by_criteria(
    msg: RabbitMessage,
    criteria: OrderFilterInput,
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_order_usecase = GetOrders(order_repo)
        outputs_list = await get_order_usecase.execute(user.id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()