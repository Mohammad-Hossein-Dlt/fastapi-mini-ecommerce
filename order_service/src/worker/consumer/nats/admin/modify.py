from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.order.modify_order_input import ModifyOrderInput
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.worker.depends.repo_depend import admin_order_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.admin.order.modify import ModifyOrder
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "order_service.admin.modify"

@client.broker.subscriber(
    subject=routing_key,
)
async def modify(
    entity: ModifyOrderInput,
    order_repo: IAdminOrderRepo = Depends(admin_order_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        get_order_usecase = ModifyOrder(order_repo)
        output = await get_order_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()
