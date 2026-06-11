import aiohttp
from src.gateway.internal.interface.Iproduct_service import IProductService
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
    
    async def get_by_id(
        self,
        access_token: str,
        product_id: str,
    ) -> dict:
                
        target_url = self.base_url + "/product/"
                
        headers = outbound_serializer(
            {
                "Authorization": f"Bearer {access_token}",
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
            params = await response.json()
            detail = params["detail"]
            raise AppBaseException(response.status, detail)
        