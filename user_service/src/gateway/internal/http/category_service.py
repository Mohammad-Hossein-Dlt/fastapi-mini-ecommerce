import aiohttp
from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.http_cleaner import clean_outbound_request

class CategoryService(ICategoryService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def get_all(
        self,
        credentials: AuthCredentials,
        category_filter: CategoryFilterInput,
    ) -> dict:
        
        target_url = self.base_url + "/get/all"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            category_filter.model_dump(mode="json"),
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
        
    async def get_one(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/get/one"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            {
                "category_id": category_id,
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