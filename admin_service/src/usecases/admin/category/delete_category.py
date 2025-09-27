from src.infra.external_api.interface.Icategory_service import ICategoryService
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteCategory:
    
    def __init__(
        self,
        category_service: ICategoryService,
    ):        
        self.category_service = category_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> OperationOutput:
        
        try:
            response: dict = self.category_service.delete_one(credentials, category_id)
            return OperationOutput.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  