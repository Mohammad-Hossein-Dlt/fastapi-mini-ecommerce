from faststream import Depends
from src.worker.consumer.nats.broker import client
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

@client.broker.subscriber(
    subject=routing_key,
)
async def create(
    entity: CreateProductInput,
    product_repo: IProductRepo = Depends(product_repo_depend),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        create_product_usecase = CreateProduct(product_repo, category_repo)
        output = await create_product_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()