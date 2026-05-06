from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.infra.exceptions.exceptions import AppBaseException


class AuthService(IAuthService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        
        self.client = client
                
        self.allowed_status_codes = [200, 201]
    
    async def get_admin(
        self,
        access_token: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=access_token,
            routing_key="auth_service.admin.get.self",
            exchange=self.client.exchange,
            timeout=10,
        )
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    async def get_user(
        self,
        access_token: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=access_token,
            routing_key="auth_service.user.get.self",
            exchange=self.client.exchange,
            timeout=10,
        )
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)