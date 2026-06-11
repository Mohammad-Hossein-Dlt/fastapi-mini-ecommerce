from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.schemas.category.update_category_input import UpdateCategoryInput
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.category.update import UpdateCategory
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.update"

@client.broker.subscriber(
    subject=routing_key,
)
async def update(
    entity: UpdateCategoryInput,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        update_category_usecase = UpdateCategory(category_repo)
        output = await update_category_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()