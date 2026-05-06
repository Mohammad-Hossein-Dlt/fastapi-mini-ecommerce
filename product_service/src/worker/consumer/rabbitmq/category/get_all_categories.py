from ._subscriber import category_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.models.schemas.filter.category_filter_input import CategoryFilterInput
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.category.get_by_criteria import GetCategories
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.get.all"

@category_subscriber(
    filter=target_routing_key(routing_key),
)
async def get_all_categories(
    msg: RabbitMessage,
    criteria: CategoryFilterInput,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_all_categories_usecase = GetCategories(category_repo)
        outputs_list = await get_all_categories_usecase.execute(criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()