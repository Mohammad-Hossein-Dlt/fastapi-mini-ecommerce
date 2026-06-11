import aiohttp
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.product.create_product_input import CreateProductInput
from src.schemas.product.update_product_input import UpdateProductInput
from src.schemas.filter.product_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer

class ProductHttpService(IProductService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def create(
        self,
        credentials: AuthCredentials,
        product: CreateProductInput,
    ) -> dict:
        
        target_url = self.base_url + "/product/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            product.model_dump(mode="json"),
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
        product_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/product/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            {
                "product_id": product_id,
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
        product: UpdateProductInput,
    ) -> dict:
        
        target_url = self.base_url + "/product/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            product.model_dump(mode="json"),
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
        product_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/product/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            {
                "product_id": product_id,
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
        criteria: ProductFilterInput,
    ) -> list:
        
        target_url = self.base_url + "/product/all"
        
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
        
        target_url = self.base_url + "/product/all"
        
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