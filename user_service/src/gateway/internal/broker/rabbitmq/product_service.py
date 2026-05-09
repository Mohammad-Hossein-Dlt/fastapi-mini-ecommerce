from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.domain.schemas.auth.auth_credentials import AuthCredentials
from src.models.schemas.filter.product_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import AppBaseException
import json

class ProductService(IProductService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
        self.check_point = "status_code"

    async def get_by_id(
        self,
        credentials: AuthCredentials,
        product_id: str,
    ) -> dict:
        
        response = await self.client.broker.request(
            message={
                "product_id": product_id,
            },
            headers={
                "token": credentials.access_token,
            },
            routing_key="product_service.product.get.by-id",
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
        criteria: ProductFilterInput,
    ) -> dict:
        
        response = await self.client.broker.request(
            message=criteria.model_dump(mode="json"),
            headers={
                "token": credentials.access_token,
            },
            routing_key="product_service.product.get.by-criteria",
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
        