from ._subscriber import product_subscriber, target_routing_key
from faststream import Depends
from faststream.rabbit import RabbitMessage
from src.models.schemas.product.create_product_input import CreateProductInput
from src.repo.interface.Iproduct_repo import IProductRepo
from src.worker.depends.repo_depend import product_repo_depend
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.product.create import CreateProduct
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.product.create"

@product_subscriber(
    filter=target_routing_key(routing_key),
)
async def create_product(
    msg: RabbitMessage,
    product: CreateProductInput,
    product_repo: IProductRepo = Depends(product_repo_depend),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        create_product_usecase = CreateProduct(product_repo, category_repo)
        output = await create_product_usecase.execute(product)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()