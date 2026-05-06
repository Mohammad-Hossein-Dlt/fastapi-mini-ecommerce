from ._subscriber import admin_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.models.schemas.order.modify_order_input import ModifyOrderInput
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.modify import ModifyOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.modify.one"

@admin_subscriber(
    filter=target_routing_key(routing_key),
)
async def modify_one_order(
    msg: RabbitMessage,
    order: ModifyOrderInput,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = ModifyOrder(order_repo)
        output = await get_order_usecase.execute(order)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
