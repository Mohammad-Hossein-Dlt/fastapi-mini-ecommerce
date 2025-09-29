from src.infra.external_api.interface.Iproduct_service import IProductService
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllProducts:
    
    def __init__(
        self,
        product_service: IProductService,
    ):        
        self.product_service = product_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        product_filter: ProductFilterInput,
    ) -> list[ProductModel]:
        
        try:
            response: dict = self.product_service.get_all(credentials, product_filter)
            return [ ProductModel.model_validate(p) for p in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  