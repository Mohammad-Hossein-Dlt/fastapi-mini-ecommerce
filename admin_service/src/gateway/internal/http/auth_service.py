import aiohttp
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.models.schemas.user.user_register_input import UserRegisterInput
from src.models.schemas.user.user_login_input import UserLoginInput
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.http_cleaner import clean_outbound_request

class AuthService(IAuthService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def register(
        self,
        user_data: UserRegisterInput,
    ) -> dict:
        
        target_url = self.base_url + "/register"
        
        user_data: dict = user_data.model_dump(mode="json")
        user_data["role"] = "admin"
                
        response = await self.session.post(
            target_url,
            json=user_data,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def login(
        self,
        user_data: UserLoginInput,
    ) -> dict:
        
        target_url = self.base_url + "/login"
        
        data = user_data.model_dump(mode="json")
        
        response = await self.session.post(
            target_url,
            data=data,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def refresh_token(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/refresh-token"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.refresh_token}",
            },
        )
        
        response = await self.session.get(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def admin_get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/admin/self/get"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        response = await self.session.get(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def admin_get_user(
        self,
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        target_url = self.base_url + "/admin/user/get"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
                
        params = clean_outbound_request(
            {
                "user_id": user_id,
                "username": username,
            },
        )
        
        response = await self.session.get(
            target_url,
            headers=headers,
            params=params,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def admin_delete_user(
        self,
        credentials: AuthCredentials,
        user_id: str | None = None,
        username: str | None = None,
    ) -> dict:
        
        target_url = self.base_url + "/admin/user/delete"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            {
                "user_id": user_id,
                "username": username,
            },
        )
        
        response = await self.session.delete(
            target_url,
            headers=headers,
            params=params,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def user_get_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/user/self/get"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        response = await self.session.get(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)
    
    async def user_delete_self(
        self,
        credentials: AuthCredentials,
    ) -> dict:
                
        target_url = self.base_url + "/user/self/delete"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        response = await self.session.delete(
            target_url,
            headers=headers,
        )
        
        if response.status in self.allowed_status_codes:
            return await response.json()
        else:
            data = await response.json()
            detail = data["detail"]
            raise AppBaseException(response.status, detail)