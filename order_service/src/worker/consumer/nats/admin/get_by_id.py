from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.get_by_id import GetOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.get.by-id"

@client.broker.subscriber(
    subject=routing_key,
)
async def get_by_id(
    order_id: int | str,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = GetOrder(order_repo)
        output = await get_order_usecase.execute(order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
