from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.schemas.category.create_category_input import CreateCategoryInput
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.dto.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.category.create import CreateCategory
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.category.create"

@client.broker.subscriber(
    subject=routing_key,
)
async def create_category(
    entity: CreateCategoryInput,
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        create_category_usecase = CreateCategory(category_repo)
        output = await create_category_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()