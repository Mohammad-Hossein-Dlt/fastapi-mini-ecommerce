from src.infra.external_api.interface.Iauth_service import IAuthService
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
        access_token: str,
        user_id: str | None = None,
        username: str | None = None,
    ) -> UserModel:
        
        try:
            user: UserModel = await self.auth_service.admin_get_user(access_token, user_id, username)
            return user
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  