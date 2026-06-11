import aiohttp
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.order.modify_order_input import ModifyOrderInput
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.schemas.order.place_order_input import PlaceOrderInput
from src.schemas.order.update_order_input import UpdateOrderInput
from src.infra.exceptions.exceptions import AppBaseException
from src.infra.utils.outbound_serializer import outbound_serializer

class OrderHttpService(IOrderService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def modify(
        self,
        credentials: AuthCredentials,
        modify: ModifyOrderInput,
    ) -> dict:
        
        target_url = self.base_url + "/admin/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            modify.model_dump(mode="json"),
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
    
    async def get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/admin/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
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
    
    async def delete_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/admin/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            {
                "order_id": order_id,
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
        criteria: OrderFilterInput,
    ) -> list:
        
        target_url = self.base_url + "/admin/all"
        
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
    
    async def delete_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> dict:
        
        target_url = self.base_url + "/admin/all"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
            criteria.model_dump(mode="json"),
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
    
    async def place_order(
        self,
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        target_url = self.base_url + "/user/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
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
    
    async def user_get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        target_url = self.base_url + "/user/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
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
    
    async def user_update(
        self,
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
       
        target_url = self.base_url + "/user/"
        
        headers = outbound_serializer(
            {
                "Authorization": f"{credentials.token_type.title()} {credentials.access_token}",
            },
        )
        
        params = outbound_serializer(
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
        
    async def user_get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        target_url = self.base_url + "/user/all"
        
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