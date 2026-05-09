import aiohttp
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.http_cleaner import clean_outbound_request

class ProductHttpService(IProductService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def get_by_id(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
                
        target_url = self.base_url + "/product/"
                
        headers = clean_outbound_request(
            {
                "Authorization": f"Bearer {access_token}",
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
            params = await response.json()
            detail = params["detail"]
            raise AppBaseException(response.status, detail)
        