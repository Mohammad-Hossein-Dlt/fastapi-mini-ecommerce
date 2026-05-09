from faststream import Depends
from src.worker.consumer.nats.broker import client
from src.repo.interface.Iproduct_repo import IProductRepo
from src.worker.depends.repo_depend import product_repo_depend
from src.domain.schemas.user.user_model import UserModel
from src.worker.depends.auth_depend import admin_auth_depend
from src.usecases.product.delete_all import DeleteProducts
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "product_service.product.delete.all"

@client.broker.subscriber(
    subject=routing_key,
)
async def delete_all(
    product_repo: IProductRepo = Depends(product_repo_depend),
    user: UserModel = Depends(admin_auth_depend),
):
    try:
        delete_all_products_usecase = DeleteProducts(product_repo)
        output = await delete_all_products_usecase.execute()
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        return ex.model_dump()
    except Exception as ex:
        return AppBaseException(status_code=500, message="Error....").model_dump()