from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.models.schemas.filter.product_filter_input import ProductFilterInput
from src.repo.interface.Iproduct_repo import IProductRepo
from src.worker.depends.repo_depend import product_repo_depend
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.worker.depends.repo_depend import category_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import user_auth_depend
from src.usecases.product.get_by_criteria import GetProducts
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.product.get.by-criteria"

@client.broker.subscriber(
    subject=routing_key,
)
async def get_by_criteria(
    criteria: ProductFilterInput,
    product_repo: IProductRepo = Depends(product_repo_depend),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    user: UserModel = Depends(user_auth_depend),
):
    try:
        get_all_products_usecase = GetProducts(product_repo, category_repo)
        outputs_list = await get_all_products_usecase.execute(criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()