from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.worker.consumer.rabbitmq.broker import subscriber
from src.worker.depends.rabbitmq_depend import target_routing_key
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.get_by_id import GetOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.get.by-id"

@subscriber(
    filter=target_routing_key(routing_key),
)
async def get_by_id(
    msg: RabbitMessage,
    order_id: int | str,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = GetOrder(order_repo)
        output = await get_order_usecase.execute(order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
