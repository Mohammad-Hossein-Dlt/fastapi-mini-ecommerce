from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.models.schemas.category.create_category_input import CreateCategoryInput
from src.domain.schemas.category.category_model import CategoryModel
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateCategory:
    
    def __init__(
        self,
        category_service: ICategoryService,
    ):        
        self.category_service = category_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        category: CreateCategoryInput,
    ) -> CategoryModel:
                
        try:
            response: dict = self.category_service.create(credentials, category)
            return CategoryModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  