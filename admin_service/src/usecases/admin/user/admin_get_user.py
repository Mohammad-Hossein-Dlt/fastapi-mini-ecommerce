from src.infra.external_api.interface.Iauth_service import IAuthService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class AdminGetUser:
    
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
    ) -> UserModel:
        
        try:
            user: dict = self.auth_service.admin_get_user(credentials, user_id, username)
            return UserModel.model_validate(user)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  