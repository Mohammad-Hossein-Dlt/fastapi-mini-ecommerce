import aiohttp
from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.category.create_category_input import CreateCategoryInput
from src.schemas.category.update_category_input import UpdateCategoryInput
from src.schemas.filter.category_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer

class CategoryHttpService(ICategoryService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
    ):
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def create(
        self,
        credentials: AuthCredentials,
        category: CreateCategoryInput,
    ) -> dict:
        
        target_url = self.base_url + "/category/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            category.model_dump(mode="json"),
        )
        
        response = await self.session.post(
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

    async def get_by_id(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/category/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
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
    
    async def update(
        self,
        credentials: AuthCredentials,
        category: UpdateCategoryInput,
    ) -> dict:
        
        target_url = self.base_url + "/category/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            category.model_dump(mode="json"),
        )
                
        response = await self.session.put(
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

    async def delete_by_id(
        self,
        credentials: AuthCredentials,
        category_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/category/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            {
                "category_id": category_id,
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
    
    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: CategoryFilterInput,
    ) -> list:
        
        target_url = self.base_url + "/category/all"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            criteria.model_dump(mode="json"),
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
        
    async def delete_all(
        self,
        credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/category/all"
        
        headers = outbound_serializer(
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