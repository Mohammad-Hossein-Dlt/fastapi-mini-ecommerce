from src.gateway.internal.interface.Iauth_service import IAuthService
from src.dto.schemas.user.user_model import UserModel

class GetUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):  
        self.auth_service = auth_service
    
    async def execute(
        self,
        access_token: str,
    ) -> UserModel:
        
        response = await self.auth_service.get_user(access_token)        
        return UserModel.model_validate(response)