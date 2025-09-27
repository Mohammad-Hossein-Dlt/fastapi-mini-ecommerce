from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.domain.schemas.category.category_model import CategoryModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllCategories:
    
    def __init__(
        self,
        category_service: ICategoryService,
    ):        
        self.category_service = category_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        category_filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        try:
            response: dict = self.category_service.get_all(credentials, category_filter)
            return [ CategoryModel.model_validate(c) for c in response ]
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  