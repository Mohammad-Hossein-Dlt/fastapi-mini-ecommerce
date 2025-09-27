from src.infra.external_api.interface.Iauth_service import IAuthService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminGetSelf:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):  
        self.auth_service = auth_service
    
    def execute(
        self,
        credentials: AuthCredentials,
    ) -> UserModel:
        
        try:
            response = self.auth_service.admin_get_self(credentials)        
            return UserModel.model_validate(response)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  