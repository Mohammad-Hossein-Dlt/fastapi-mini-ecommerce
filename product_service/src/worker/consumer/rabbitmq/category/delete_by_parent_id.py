from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.worker.consumer.rabbitmq.broker import subscriber
from src.worker.depends.rabbitmq_depend import target_routing_key
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.category.delete_by_parent_id import DeleteCategories
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.delete.all"

@subscriber(
    filter=target_routing_key(routing_key),
)
async def delete_by_parent_id(
    msg: RabbitMessage,
    parent_id: str,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_categories_usecase = DeleteCategories(category_repo)
        output = await delete_all_categories_usecase.execute(parent_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()