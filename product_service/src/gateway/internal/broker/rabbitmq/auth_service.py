from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.infra.exceptions.exceptions import AppBaseException

class AuthService(IAuthService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
    
    async def get_admin(
        self,
        access_token: str,
    ) -> dict:
        
        try:
            return await self.client.broker.request(
                headers={
                    "token": access_token,
                },
                routing_key="auth_service.admin.get.self",
                exchange=self.client.exchange,
                timeout=10,
            )
        except:
            raise
    
    async def get_user(
        self,
        access_token: str,
    ) -> dict:
        
        try:
            return await self.client.broker.request(
                headers={
                    "token": access_token,
                },
                routing_key="auth_service.user.get.self",
                exchange=self.client.exchange,
                timeout=10,
            )
        except:
            raise