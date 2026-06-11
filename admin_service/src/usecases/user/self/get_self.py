from src.gateway.internal.interface.Iauth_service import IAuthService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.dto.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetSelf:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):  
        self.auth_service = auth_service
    
    async def execute(
        self,
        credentials: AuthCredentials,
    ) -> UserModel:
        
        try:
            response = await self.auth_service.user_get_self(credentials)        
            return UserModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  