from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.worker.consumer.rabbitmq.broker import subscriber
from src.worker.depends.rabbitmq_depend import target_routing_key
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.category.get_by_id import GetCategory
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.get.by-id"

@subscriber(
    filter=target_routing_key(routing_key),
)
async def get_by_id(
    msg: RabbitMessage,
    category_id: str,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_category_usecase = GetCategory(category_repo)
        output = await get_category_usecase.execute(category_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()