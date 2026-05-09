from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.category.delete_by_parent_id import DeleteCategories
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.delete.all"

@client.broker.subscriber(
    subject=routing_key,
)
async def delete_by_parent_id(
    parent_id: str,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_categories_usecase = DeleteCategories(category_repo)
        output = await delete_all_categories_usecase.execute(parent_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()