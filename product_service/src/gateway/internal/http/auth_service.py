import aiohttp
from src.gateway.internal.interface.Iauth_service import IAuthService
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer

class AuthHttpService(IAuthService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def get_admin(
        self,
        access_token: str,
    ) -> dict:
        
        target_url = self.base_url + "/admin/self/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"Bearer {access_token}",
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
    
    async def get_user(
        self,
        access_token: str,
    ) -> dict:
        
        target_url = self.base_url + "/user/self/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"Bearer {access_token}",
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