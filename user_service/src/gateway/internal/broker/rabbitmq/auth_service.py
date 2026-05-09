from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException
import json

class AuthService(IAuthService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
        self.check_point = "status_code"
    
    async def register(
        self,
        user: UserRegisterInput,
    ) -> dict:
        
        message = user.model_dump()
        message["role"] = "admin"
        response = await self.client.broker.request(
            message=message,
            routing_key="auth_service.auth.register",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
    
    async def login(
        self,
        user: UserLoginInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=user.model_dump(),
            routing_key="auth_service.auth.login",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
    
    async def refresh_token(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        response = await self.client.broker.request(
            headers={
                "token": credentials.refresh_token,
            },
            routing_key="auth_service.auth.refresh-token",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
  
    async def get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        response = await self.client.broker.request(
            headers={
                "token": credentials.access_token,
            },
            routing_key="auth_service.user.get.self",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
    
    async def delete_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        response = await self.client.broker.request(
            headers={
                "token": credentials.access_token,
            },
            routing_key="auth_service.user.delete.self",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict