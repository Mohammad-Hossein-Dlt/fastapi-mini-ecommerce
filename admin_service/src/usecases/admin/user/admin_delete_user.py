from src.infra.external_api.interface.Iauth_service import IAuthService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminDeleteUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):
        
        self.auth_service = auth_service    
    
    async def execute(
        self,
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> OperationOutput:
        
        try:
            response: dict = self.auth_service.admin_delete_user(credentials, user_id, username)
            return OperationOutput.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  