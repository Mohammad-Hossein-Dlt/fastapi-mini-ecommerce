import aiohttp
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.filter_order_input import UserFilterOrderInput
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.models.schemas.order.update_order_input import UpdateOrderInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.http_cleaner import clean_outbound_request

class OrderService(IOrderService):
        
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def user_place_order(
        self,
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        target_url = self.base_url + "/user/place-order"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            order.model_dump(mode="json"),
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
    
    
    async def user_get_one(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/user/get/one"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            {
                "order_id": order_id,
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
    
    
    async def user_get_all(
        self,
        credentials: AuthCredentials,
        order_filter: UserFilterOrderInput,
    ) -> dict:
        
        target_url = self.base_url + "/user/get/all"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            order_filter.model_dump(mode="json"),
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
    
    async def user_update_one(
        self,
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
       
        target_url = self.base_url + "/user/update/one"
        
        headers = clean_outbound_request(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = clean_outbound_request(
            order.model_dump(mode="json"),
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