from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.models.schemas.filter.category_filter_input import CategoryFilterInput
from src.domain.schemas.category.category_model import CategoryModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetCategories:
    
    def __init__(
        self,
        category_service: ICategoryService,
    ):        
        self.category_service = category_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        criteria: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        try:
            response: dict = await self.category_service.get_by_criteria(credentials, criteria)
            return [ CategoryModel.model_validate(c) for c in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  