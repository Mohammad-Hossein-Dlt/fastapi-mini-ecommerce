from src.infra.external_api.interface.Iproduct_service import IProductService
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetProduct:
    
    def __init__(
        self,
        product_service: IProductService,
    ):        
        self.product_service = product_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        product_id: str,
    ) -> ProductModel:
        
        try:
            response: dict = self.product_service.get_one(credentials, product_id)
            return ProductModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  