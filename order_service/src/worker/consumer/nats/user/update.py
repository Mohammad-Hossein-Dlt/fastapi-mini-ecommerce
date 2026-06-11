from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.schemas.order.update_order_input import UpdateOrderInput
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.worker.depends.repo_depend import user_order_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.user.order.update import UpdateOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.user.update"

@client.broker.subscriber(
    subject=routing_key,
)
async def update(
    entity: UpdateOrderInput,
    order_repo: IOrderRepo = Depends(user_order_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_order_usecase = UpdateOrder(order_repo)
        output = await get_order_usecase.execute(user, entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()