from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import user_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.user.order.get_by_id import GetOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.user.get.by-id"

@client.broker.subscriber(
    subject=routing_key,
)
async def get_by_id(
    order_id: str,
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_order_usecase = GetOrder(order_repo)
        output = await get_order_usecase.execute(user, order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
