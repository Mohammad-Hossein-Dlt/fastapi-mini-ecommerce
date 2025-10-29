from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.schemas.broker.rabbitmq_params import RabbitParams
from faststream.rabbit import RabbitBroker, RabbitExchange, ExchangeType
from src.infra.exceptions.exceptions import AppBaseException


class AuthService(IAuthService):
    
    def __init__(
        self,
        params: RabbitParams,
    ):
        self.broker = RabbitBroker(url=params.url)
        self.exchange = RabbitExchange(name=params.exchange,type=ExchangeType.TOPIC)
        
        self.allowed_status_codes = [200, 201]
    
    async def admin_get_self(
        self,
        access_token: str,
    ) -> dict:
        
        response = await self.broker.request(
            message=access_token,
            routing_key="auth_service.admin.get.self",
            exchange=self.exchange,
            timeout=10,
        )
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)
    
    async def user_get_self(
        self,
        access_token: str,
    ) -> dict:
        
        response = await self.broker.request(
            message=access_token,
            routing_key="auth_service.user.get.self",
            exchange=self.exchange,
            timeout=10,
        )
        
        if response.status_code in self.allowed_status_codes:
            return response.json()
        else:
            data = response.json()
            detail = data["detail"]
            raise AppBaseException(response.status_code, detail)