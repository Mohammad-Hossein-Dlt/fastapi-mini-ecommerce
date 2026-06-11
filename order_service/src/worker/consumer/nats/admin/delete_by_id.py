from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.delete_by_id import DeleteOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.delete.by-id"

@client.broker.subscriber(
    subject=routing_key,
)
async def delete_by_id(
    order_id: str,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = DeleteOrder(order_repo)
        output = await get_order_usecase.execute(order_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
