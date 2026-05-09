from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.gateway.internal.interface.Iorder_service import IOrderService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.models.schemas.order.place_order_input import PlaceOrderInput
from src.models.schemas.order.update_order_input import UpdateOrderInput
from src.infra.exceptions.exceptions import AppBaseException
import json

class OrderService(IOrderService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
        self.check_point = "status_code"
    
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
            routing_key="order_service.user.place-order",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
    
    async def get_by_id(
        self,
        credentials: AuthCredentials,
        order_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message={
                "order_id": order_id,
            },
            headers={
                "token": credentials.access_token,
            },
            routing_key="order_service.user.get.by-id",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
    
    async def update(
        self,
        credentials: AuthCredentials,
        order: UpdateOrderInput,
    ) -> dict:
       
        response = await self.client.broker.request(
            message=order.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            routing_key="order_service.user.update",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict
        
    async def get_by_criteria(
        self,
        credentials: AuthCredentials,
        criteria: OrderFilterInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            routing_key="order_service.user.get.by-criteria",
            exchange=self.client.exchange,
            timeout=10,
        )
        _dict: dict = json.loads(response.body.decode())
        status = _dict.get(self.check_point, None)
        if status:
            message = _dict.get("message", None)
            raise AppBaseException(status, message)
        else:
            return _dict