from src.gateway.internal.interface.Iproduct_service import IProductService
from src.dto.schemas.product.product_model import ProductModel
from src.dto.schemas.auth.auth_credentials import AuthCredentials
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
            response: dict = await self.product_service.get_by_id(credentials, product_id)
            return ProductModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  