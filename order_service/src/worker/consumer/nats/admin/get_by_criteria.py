from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.get_by_criteria import GetOrders
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.get.by-criteria"

@client.broker.subscriber(
    subject=routing_key,
)
async def get_by_criteria(
    criteria: OrderFilterInput,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = GetOrders(order_repo)
        outputs_list = await get_order_usecase.execute(criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
