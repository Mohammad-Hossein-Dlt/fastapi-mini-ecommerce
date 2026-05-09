from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.schemas.broker.nats import NatsClient
from src.infra.exceptions.exceptions import AppBaseException
import json

class AuthBrokerService(IAuthService):
    
    def __init__(
        self,
        client: NatsClient,
    ):
        self.client = client
        self.check_point = "status_code"
    
    async def get_admin(
        self,
        access_token: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=None,
            headers={
                "token": access_token,
            },
            subject="auth_service.admin.get.self",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def get_user(
        self,
        access_token: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=None,
            headers={
                "token": access_token,
            },
            subject="auth_service.user.get.self",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data