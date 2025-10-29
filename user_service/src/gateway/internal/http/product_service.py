import aiohttp
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.http_cleaner import clean_outbound_request

class ProductService(IProductService):
    
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
        product_filter: ProductFilterInput,
    ) -> dict:
        
        target_url = self.base_url + "/get/all"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            product_filter.model_dump(mode="json"),
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
        product_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/get/one"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
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