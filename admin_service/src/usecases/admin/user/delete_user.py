from src.gateway.internal.interface.Iauth_service import IAuthService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteUser:
    
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
            response: dict = await self.auth_service.admin_delete_user(credentials, user_id, username)
            return OperationOutput.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  