from src.gateway.internal.interface.Iproduct_service import IProductService
from src.models.schemas.filter.product_filter_input import ProductFilterInput
from src.domain.schemas.product.product_model import ProductModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetProducts:
    
    def __init__(
        self,
        product_service: IProductService,
    ):        
        self.product_service = product_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        criteria: ProductFilterInput,
    ) -> list[ProductModel]:
        
        try:
            response: dict = await self.product_service.get_by_criteria(credentials, criteria)
            return [ ProductModel.model_validate(p) for p in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  