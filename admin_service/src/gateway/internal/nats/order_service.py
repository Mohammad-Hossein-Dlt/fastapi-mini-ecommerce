from src.gateway.internal.interface.Iorder_service import IOrderService
from src.infra.schemas.broker.nats import NatsClient
from src.dto.schemas.auth.auth_credentials import AuthCredentials
from src.schemas.order.modify_order_input import ModifyOrderInput
from src.schemas.filter.order_filter_input import OrderFilterInput
from src.schemas.order.place_order_input import PlaceOrderInput
from src.schemas.order.update_order_input import UpdateOrderInput
from src.infra.exceptions.exceptions import AppBaseException
import json

class OrderBrokerService(IOrderService):
    
    def __init__(
        self,
        client: NatsClient,
    ):
        self.client = client
        self.check_point = "status_code"
    
    async def modify(
        self,
        credentials: AuthCredentials,
        modify: ModifyOrderInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=modify.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.admin.modify",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=order_id,
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.admin.get.by-id",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def delete_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=order_id,
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.admin.delete.by-id",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
        
    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.admin.get.by-criteria",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def delete_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.admin.delete.by-criteria",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def place_order(
        self,
        credentials: AuthCredentials,
        order: PlaceOrderInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=order.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.user.place-order",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def user_get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=order_id,
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.user.get.by-id",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
    
    async def user_update(
        self,
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
       
        response = await self.client.broker.request(
            message=order.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.user.update",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data
        
    async def user_get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> list:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            subject="order_service.user.get.by-criteria",
            timeout=10,
        )
        
        data = json.loads(response.body.decode())
        status = False
        if isinstance(data, dict):
            status = data.get(self.check_point, False)
            
        if status:
            message = data.get("message", None)
            raise AppBaseException(status, message)
        else:
            return data