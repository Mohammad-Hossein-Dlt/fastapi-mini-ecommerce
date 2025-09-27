from src.infra.external_api.interface.Iproduct_service import IProductService
from src.models.schemas.product.update_product_input import UpdateProductInput
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateProduct:
    
    def __init__(
        self,
        product_service: IProductService,
    ):        
        self.product_service = product_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        product: UpdateProductInput,
    ) -> ProductModel:
        
        try:
            response: dict = self.product_service.update_one(credentials, product)
            return ProductModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  