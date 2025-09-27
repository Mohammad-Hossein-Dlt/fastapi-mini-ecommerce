from src.infra.external_api.interface.Iauth_service import IAuthService
from src.domain.schemas.user.user_model import UserModel

class UserGetSelf:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):  
        self.auth_service = auth_service
    
    def execute(
        self,
        access_token: str,
    ) -> UserModel:
        response = self.auth_service.user_get_self(access_token)        
        return UserModel.model_validate(response)