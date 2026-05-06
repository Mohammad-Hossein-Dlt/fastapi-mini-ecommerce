from ._subscriber import admin_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.delete_by_criteria import DeleteOrders
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.delete.all"

@admin_subscriber(
    filter=target_routing_key(routing_key),
)
async def delete_all_orders(
    msg: RabbitMessage,
    criteria: FilterOrderInput,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = DeleteOrders(order_repo)
        output = await get_order_usecase.execute(criteria)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
