from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.schemas.broker.nats import NatsClient
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException
import json

class AuthBrokerService(IAuthService):
    
    def __init__(
        self,
        client: NatsClient,
    ):
        self.client = client
        self.check_point = "status_code"
    
    async def register(
        self,
        user: UserRegisterInput,
    ) -> dict:
        
        message = user.model_dump()
        message["role"] = "user"
        response = await self.client.broker.request(
            message=message,
            subject="auth_service.auth.register",
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
    
    async def login(
        self,
        user: UserLoginInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=user.model_dump(),
            subject="auth_service.auth.login",
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
    
    async def refresh_token(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        response = await self.client.broker.request(
            message=None,
            headers={
                "token": credentials.refresh_token,
            },
            subject="auth_service.auth.refresh-token",
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
  
    async def get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=None,
            headers={
                "token": credentials.access_token,
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
    
    async def delete_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        response = await self.client.broker.request(
            message=None,
            headers={
                "token": credentials.access_token,
            },
            subject="auth_service.user.delete.self",
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