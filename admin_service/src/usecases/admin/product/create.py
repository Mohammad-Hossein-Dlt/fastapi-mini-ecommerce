from src.gateway.internal.interface.Iproduct_service import IProductService
from src.models.schemas.product.create_product_input import CreateProductInput
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateProduct:
    
    def __init__(
        self,
        product_service: IProductService,
    ):        
        self.product_service = product_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        entity: CreateProductInput,
    ) -> ProductModel:

        try:
            response: dict = await self.product_service.create(credentials, entity)
            return ProductModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  