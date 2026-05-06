from ._subscriber import category_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.category.update import UpdateCategory
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.update.one"

@category_subscriber(
    filter=target_routing_key(routing_key),
)
async def update_one_category(
    msg: RabbitMessage,
    category: UpdateCategoryInput,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        update_category_usecase = UpdateCategory(category_repo)
        output = await update_category_usecase.execute(category)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()