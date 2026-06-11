from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.dto.schemas.category.category_model import CategoryModel
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetCategory:
    
    def __init__(
        self,
        category_service: ICategoryService,
    ):        
        self.category_service = category_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> CategoryModel:
        
        try:
            response: dict = await self.category_service.get_by_id(credentials, category_id)
            return CategoryModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")