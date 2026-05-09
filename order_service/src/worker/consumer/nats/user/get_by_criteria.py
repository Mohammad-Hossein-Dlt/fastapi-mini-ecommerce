from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import user_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.user.order.get_by_criteria import GetOrders
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.user.get.by-criteria"

@client.broker.subscriber(
    subject=routing_key,
)
async def get_by_criteria(
    criteria: OrderFilterInput,
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_order_usecase = GetOrders(order_repo)
        outputs_list = await get_order_usecase.execute(user, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()